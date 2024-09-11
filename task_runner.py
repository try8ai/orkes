from conductor.client.configuration.configuration import Configuration
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.workflow.executor.workflow_executor import StartWorkflowRequest

def main():
    api_config = Configuration()
    workflow_executor = WorkflowExecutor(configuration=api_config)

    workflow_req = StartWorkflowRequest(name="greetings", version=1, input={"name": "orkes"})
    workflow_run = workflow_executor.start_workflow(workflow_req)

    print(f'\nworkflow result: {workflow_run}\n')
    print(f'see the workflow execution here: {api_config.ui_host}/execution/{workflow_req}\n')

if __name__ == '__main__':
    main()
