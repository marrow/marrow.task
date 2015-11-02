# encoding: utf-8

""""""

from concurrent.futures._base import Future

from .model import Task
from .message import TaskMessage


log = __import__('logging').getLogger(__name__)


def _execute_callback(callable, task):
	pass


class TaskFuture(Future):
	"""concurrent.futures.Future-like compatible wrapper of :class:`.Task`"""

	__slots__ = ('_task', )

	def __init__(self, task):
		""":param task: :class:`.Task` instance or it's id"""
		self._task = getattr(task, 'pk', task)
	
	@property
	def task(self):
		return Task.objects.get(id=self._task)
	
	@property
	def messages(self):
		return TaskMessage.objects(task=self._task)
	
	def _invoke_callbacks(self):
		self.task._invoke_callbacks()
	
	def __repr__(self):
		return '<Task %s state=%s>' % (self._task, self.task.state)
	
	def cancel(self):
		"""Cancel the future if possible."""
		return Task.cancel(self._task)
	
	def cancelled(self):
		return bool(Task.objects.cancelled(id=self._task))
	
	def running(self):
		return bool(Task.objects.running(id=self._task))
	
	def done(self):
		return bool(Task.objects.finished(id=self._task))
	
	def add_done_callback(self, fn):
		self.task.add_callback(fn, iteration=False)
	
	def result(self, timeout=None):
		return self.task.wait(timeout).result

	def exception(self, timeout=None):
		return self.task.wait(timeout).exception

	def set_running_or_notify_cancel(self):
		return self.task.set_running_or_notify_cancel()

	def set_result(self, result):
		self.task.set_result(result)

	def set_exception(self, exception):
		self.task.set_exception(exception)