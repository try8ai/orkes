# Hello World Application Using Conductor

In this section, we will create a simple "Hello World" application that executes a "greetings" workflow managed by Conductor.

### Step 1: Create Workflow

Create `greetings_workflow.py` with the following:

<insert-text file="greetings_workflow.py" line="0" col="0">
```python
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from greetings_worker import greet

def greetings_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    name = 'greetings'
    workflow = ConductorWorkflow(name=name, executor=workflow_executor)
    workflow.version = 1
    workflow.owner_email("me@example.com")
    workflow >> greet(task_ref_name='greet_ref', name=workflow.input('name'))
    return workflow
```
</insert-text>

### Step 2: Write Task Worker
Using Python, a worker represents a function with the worker_task decorator. Create `greetings_worker.py` file as illustrated below:

note
A single workflow can have task workers written in different languages and deployed anywhere, making your workflow polyglot and distributed!

<insert-text file="greetings_worker.py" line="0" col="0">
```python
from conductor.client.worker.worker_task import worker_task


@worker_task(task_definition_name='greet')
def greet(name: str) -> str:
    return f'Hello {name}'
```
</insert-text>

Now, we are ready to write our main application, which will execute our workflow.

### Step 3: Write Greetings Runner

<insert-text file="greetings_runner.py" line="0" col="0">
```python
from conductor.client.configuration.configuration import Configuration
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.executor.workflow_executor import StartWorkflowRequest
from greetings_workflow import greetings_workflow

def main():
    api_config = Configuration()
    workflow_executor = WorkflowExecutor(configuration=api_config)

	# Register the workflow - required only the first time this is run
    workflow = greetings_workflow(workflow_executor=workflow_executor)
    workflow.register(True)

    workflow_req = StartWorkflowRequest(name="greetings", version=1, input={"name": "orkes"})
    workflow_run = workflow_executor.start_workflow(workflow_req)

    print(f'\nworkflow result: {workflow_run}\n')
    print(f'see the workflow execution here: {api_config.ui_host}/execution/{workflow_req}\n')

if __name__ == '__main__':
    main()
```
</insert-text>

Now run the application!

<button data-command="python greetings_runner.py">`python greetings_runner.py`</button>

After running, you can navigate to the conductor UI via the `5000-tcp` endpoint. In the **Executions** tab, you should see the workflow status as `RUNNING`. It will not complete yet because there is nothing processing started workflows.

To complete the workflow, let's add `workflow_runner.py` with a `main` method:

<insert-text file="workflow_runner.py" line="0" col="0">
```python
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor

def main():
    # The app is connected to http://localhost:8080/api by default
    api_config = Configuration()

    workflow_executor = WorkflowExecutor(configuration=api_config)

    # Starting the worker polling mechanism
    task_handler = TaskHandler(configuration=api_config)
    task_handler.start_processes()

if __name__ == '__main__':
    main()
```
</insert-text>

Now start the workflow runner:

<button data-command="python workflow_runner.py">`python workflow-runner.py`</button>

Now if you refresh the Conductor UI, you should see that the runner has picked up the execution that was started earlier and completed it!
