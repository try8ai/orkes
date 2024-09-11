# Orkes Conductor Python SDK

Orkes Conductor Python SDK is maintained here: https://github.com/conductor-sdk/conductor-python.

## Install Conductor Python SDK

Before installing Conductor Python SDK, it is a good practice to set up a dedicated virtual environment as follows:

```
virtualenv conductor
source conductor/bin/activate
```

# Get Conductor Python SDK
The SDK requires Python 3.9+. To install the SDK, use the following command:

```
python3 -m pip install conductor-python
```

## Hello World Application Using Conductor

In this section, we will create a simple "Hello World" application that executes a "greetings" workflow managed by Conductor.

### Step 1: Create Workflow
#### Creating Workflows by Code

Create `greetings_workflow.py` with the following:

```
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from greetings_worker import greet

def greetings_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    name = 'greetings'
    workflow = ConductorWorkflow(name=name, executor=workflow_executor)
    workflow.version = 1
    workflow >> greet(task_ref_name='greet_ref', name=workflow.input('name'))
    return workflow
```

### Step 2: Write Task Worker
Using Python, a worker represents a function with the worker_task decorator. Create `greetings_worker.py` file as illustrated below:

note
A single workflow can have task workers written in different languages and deployed anywhere, making your workflow polyglot and distributed!

```
from conductor.client.worker.worker_task import worker_task


@worker_task(task_definition_name='greet')
def greet(name: str) -> str:
    return f'Hello {name}'
```

Now, we are ready to write our main application, which will execute our workflow.

### Step 3: Write Hello World Application
Let's add `helloworld.py` with a `main` method:

```
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from greetings_workflow import greetings_workflow


def register_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    workflow = greetings_workflow(workflow_executor=workflow_executor)
    workflow.register(True)
    return workflow


def main():
    # The app is connected to http://localhost:8080/api by default
    api_config = Configuration()

    workflow_executor = WorkflowExecutor(configuration=api_config)

    # Registering the workflow (Required only when the app is executed the first time)
    workflow = register_workflow(workflow_executor)

    # Starting the worker polling mechanism
    task_handler = TaskHandler(configuration=api_config)
    task_handler.start_processes()

    workflow_run = workflow_executor.execute(name=workflow.name, version=workflow.version,
                                             workflow_input={'name': 'Orkes'})

    print(f'\nworkflow result: {workflow_run.output["result"]}\n')
    print(f'see the workflow execution here: {api_config.ui_host}/execution/{workflow_run.workflow_id}\n')
    task_handler.stop_processes()


if __name__ == '__main__':
    main()
```


### Running Workflows on Conductor

#### Setup Environment Variable
Set the following environment variable to point the SDK to the Conductor Server API endpoint:

```
export CONDUCTOR_SERVER_URL=http://localhost:8080/api
```

#### Execute Hello World Application
To run the application, type the following command:

```
python helloworld.py
```

Now, the workflow is executed, and its execution status can be viewed from Conductor UI (http://localhost:5000).

Navigate to the **Executions** tab to view the workflow execution.

Open the Workbench tab and try running the 'greetings' workflow. You will notice that the workflow execution fails. This is because the task_handler.stop_processes() [helloworld.py] function is called and stops all workers included in the app, and therefore, there is no worker up and running to execute the tasks.

Now, let's update the app `helloworld.py`.

```
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from greetings_workflow import greetings_workflow


def register_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    workflow = greetings_workflow(workflow_executor=workflow_executor)
    workflow.register(True)
    return workflow


def main():
    # points to http://localhost:8080/api by default
    api_config = Configuration()

    workflow_executor = WorkflowExecutor(configuration=api_config)

    # Needs to be done only when registering a workflow one-time
    # workflow = register_workflow(workflow_executor)

    task_handler = TaskHandler(configuration=api_config)
    task_handler.start_processes()

    # workflow_run = workflow_executor.execute(name=workflow.name, version=workflow.version,
                                             workflow_input={'name': 'World'})

    # print(f'\nworkflow result: {workflow_run.output["result"]}\n')
    # print(f'see the workflow execution here: {api_config.ui_host}/execution/{workflow_run.workflow_id}\n')
    
    # task_handler.stop_processes()


if __name__ == '__main__':
    main()
```

By commenting the lines that execute the workflow and stop the task polling mechanism, we can re-run the app and run the workflow from the Conductor UI. The task is executed successfully.
