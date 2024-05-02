from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
)
from rich.text import Text

if TYPE_CHECKING:
    from exemplify.steps.base import Step


console = Console()


class HiddenSpinnerColumn(SpinnerColumn):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text

    def render(self, task):
        text = self.text.format(task=task)

        if task.started and not task.finished:
            return f"{self.spinner.render(task.get_time())}  {text}"

        if not task.started:
            return f":heavy_minus_sign: {text}"

        return text


class HiddenTimeElapsedColumn(TimeElapsedColumn):
    def render(self, task):
        return super().render(task) if task.started and not task.finished else Text("")


@dataclass
class StepInfo:
    task_id: TaskID
    step: "Step"
    output: list[str] = field(default_factory=list)
    ret: Optional[int] = None
    display_output: bool = False


class StepProgress(Progress):
    def __init__(self, display_output=False, **kwargs):
        self._cur_index = -1
        self._steps = []
        self.display_output = display_output
        return super().__init__(
            TextColumn(" "),
            HiddenSpinnerColumn("{task.description}", spinner_name="dots"),
            **kwargs,
        )

    def add_step(self, step: "Step") -> None:
        task_id = self.add_task(str(step), start=False, visible=False)
        self._steps.append(StepInfo(task_id, step, display_output=self.display_output))

    @property
    def current(self) -> StepInfo:
        return self._steps[self._cur_index]

    def __next__(self) -> "Step":
        if self._cur_index >= 0:
            self.stop_task(self.current.task_id)
            self.update(advance=1)

        self._cur_index += 1
        try:
            info = self.current
        except IndexError:
            raise StopIteration

        self.update(total=1)
        self.start_task(info.task_id)
        return info.step

    def start(self):
        for info in self._steps:
            super().update(info.task_id, visible=True)

    def update(self, *args, **kwargs):
        info = self.current

        if not kwargs.get("description"):
            emoji = ""
            if info.ret is not None:
                emoji = ":white_heavy_check_mark: " if info.ret == 0 else ":x: "

            desc = [f"{emoji}{info.step}"]
            if info.display_output:
                desc.extend(info.output)
            kwargs["description"] = "\n".join(desc)

        super().update(info.task_id, *args, **kwargs)

    def append_output(self, output: str) -> None:
        self.current.output.append(console.render_str(output).markup)
        if self.current.display_output:
            self.update()

    def set_status(self, ret: int) -> None:
        self.current.ret = ret
        if ret != 0:
            self.current.display_output = True
            self.update()


class RoutineProgress(Progress):
    def __init__(self, routine, display_output=False, **kwargs):
        self.routine = routine
        self.step = StepProgress(display_output=display_output)
        super().__init__(
            TextColumn("{task.description}"), HiddenTimeElapsedColumn(), **kwargs
        )

        self._id = self.add_task(f"[bold]Routine {self.routine}", start=False)

    @property
    def returncode(self):
        returncode = 0
        for info in self.step._steps:
            if info.ret is None:
                return None
            returncode |= info.ret
        return returncode

    def update(self, *args, **kwargs):
        return super().update(self._id, *args, **kwargs)

    def start_routine(self) -> None:
        self.step.start()
        self.start_task(self._id)
        self.update(
            description=f"[bold]Routine [blue]{self.routine}[/blue] processing.."
        )

    def stop_routine(self) -> None:
        self.stop_task(self._id)

        if self.returncode == 0:
            description = f"[bold green]Routine [blue]{self.routine}[/blue] succeeded!"
        else:
            description = f"[bold red]Routine [blue]{self.routine}[/blue] failed!"
        self.update(description=description)
