from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.text import Text

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


class StepProgress(Progress):
    def __init__(self, **kwargs):
        self._current = -1
        self.steps = []
        return super().__init__(
            TextColumn(" "),
            HiddenSpinnerColumn("{task.description}", spinner_name="dots"),
            **kwargs,
        )

    def add_step(self, step: Step) -> None:
        task_id = self.add_task(str(step), start=False, visible=False)
        self.steps.append((task_id, step))

    def __next__(self) -> Step:
        if self._current >= 0:
            task_id, step = self.steps[self._current]
            self.stop_task(task_id)
            self.update(advance=1)

        self._current += 1
        try:
            task_id, step = self.steps[self._current]
        except IndexError:
            raise StopIteration

        self.update(total=1)
        self.start_task(task_id)
        return step

    def start(self):
        for task_id, _ in self.steps:
            super().update(task_id, visible=True)

    def update(self, *args, **kwargs):
        task_id, _ = self.steps[self._current]
        super().update(task_id, *args, **kwargs)


class RoutineProgress(Progress):
    def __init__(self, routine, **kwargs):
        self.returncode = 0
        self.routine = routine
        self.step = StepProgress()
        super().__init__(
            TextColumn("{task.description}"), HiddenTimeElapsedColumn(), **kwargs
        )

        self._id = self.add_task(f"Routine {self.routine}", start=False)

    def update(self, *args, **kwargs):
        return super().update(self._id, *args, **kwargs)

    def start_routine(self):
        self.step.start()
        self.start_task(self._id)

    def stop_routine(self):
        self.stop_task(self._id)
