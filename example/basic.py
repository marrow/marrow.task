# encoding: utf-8

"""Basic sample tasks.

To use these, be sure to start an interactive shell and import the module.
"""

from __future__ import unicode_literals, print_function


from marrow.task import task, Task



# Decorated task; no configuration.
# Does *not* defer by default: the hello function is directly returned, after annotation.

@task
def hello(name):
	# Context is a (threading.locals) thread-local pool constructed by the decorator.
	# This context normally contains:
	#  * id - the ObjectId of the task being executed
	#  * task - a lazily-
	# Execution (immediate, deferred, whatever) provides the ObjectId representing this execution, or None
	# if running locally.
	return "Hello, " + name + " I'm " + (hello.context.id or 'running locally')


# Bare function.

def mul(x, y):
	return x * y


# Deferred execution by default.

@task(defer=True)
def farewell(name):
	return "Farewell " + name + "."


@task(defer=True)
def count(n):
	for i in range(n):
		yield n


def emit(task):
	print(task.result)


def run():
	
	# Not Deferred by Default
	# Executing a decorated function, same as hello.call(None, *args, **kw)
	hello("world")
	
	# Explicitly calling. This is used internally by the runner. First positional argument is a Task instance
	# or the ObjectId of a Task instance, or None for local execution.  (This sets up the thread-local context
	# amongst other things like setting the return value and capturing any exceptions.)
	hello.call(None, "world")  # Keyword arguments would work, too.
	
	# Explicitly deferring, well, defers.  Returns a Task instance for this task.
	task = hello.defer("world")
	
	# There are several things you can do with a task instance:
	task.wait()  # Wait forever for completion (of any kind).
	task.wait(30)  # Wait 30 seconds.
	
	# The completion messages contain the results, so waiting will update the local task instance with the result
	# or exception as appropriate, plus the waiting/running/completed/successful/failed times and thus booleans.
	
	task.waiting  # True if the task hasn't been picked up by a worker yet.
	task.running  # True if the task is still processing.
	task.completed  # True if the task has finished.
	task.successful  # True if the task exited cleanly.
	task.failed  # True if there was an exception raised.
	
	print(task.result)  # Finally emit the result. If not finished, wait forever for the result.
	
	# If there was an exception, attempting to get task.result would explode. The resulting explosion will be the
	# original exception and traceback, on Python 3 with one of those "while processing X exception, this other one
	# occurred".
	
	# This would also contain the exception details: exception class, arguments, and traceback representation.
	# (This lets the exception instance itself be recreated.)
	task.exception
	
	# Scheduled deferring.  Returns a Task instance for this task.
	# Exact datetime.  Timezone aware, naive assumed to be UTC.
	hello.at(datetime.utcnow() + timedelta(minutes=1), "world")
	
	# Relative deferring.  Returns a Task instance.
	# Useful for scheduling an action you want to give the user some "grace time" to cancel.
	hello.after(timedelta(minutes=1), "world")
	
	# Deferred by default returns a Task instance.
	# Explicitly calling, as well as scheduled and relative deferring are the same as above.
	farewell("cruel world")
	
	# Bare functions are bare functions...
	mul(2, 4)
	
	# Bare functions can be deferred using Task classmethod factories.
	task(mul).defer(2, 4)
	task(mul).at(datetime.utcnow(), 4, 8)
	task(mul).after(timedelta(seconds=30), 2, 12)
	
	# Deferred generators work, too.
	task = count(10)
	
	# Register a callback; if the task is already finished, submit the callback with a DBRef to the task as the
	# argument.  DBRef arguments to submitted tasks are dereferenced automatically prior to calling the task.
	task.add_callback(emit)
	
	
	# There are some useful helpers:
	
	task = hello.defer("world")
	str(task)  # wait forever to get the result, then str() it
	int(task)  # same
	float(task)  # same
	bytes(task)  # same (though Python 2 compatibility means str()/unicode() differs slightly)
	
	task = count(10)
	list(task)  # same, piggy-backs on iteration
	
	# as long as the capped collection is large enough, reiteration should be A-OK
	for i in task:
		pass  # same, but progressively, as each yield is issued by the task
	
	# You can even use arbitrary dot-colon function references.
	task('basic:farewell').call("cruel world")
	
	
	# Task.retries  # The maximum number of retries.
	# Task.delay  # The number of seconds to wait before starting execution.
	# Task.rate  # The maximum number of this task to process.  (10, 2, 'hour'), 10 every two hours.
