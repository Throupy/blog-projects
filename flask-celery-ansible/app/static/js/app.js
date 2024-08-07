document.addEventListener('DOMContentLoaded', function () {
    var startTaskButton = document.getElementById('startTaskButton');
    var loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'), {
        backdrop: 'static',
        keyboard: false
    });
    var taskStatus = document.getElementById('taskStatus');
    var taskOutput = document.getElementById('taskOutput');
    var progressBar = document.getElementById('progressBar');

    startTaskButton.addEventListener('click', function () {
        fetch('/start_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function (response) {
            return response.json();
        }).then(function (data) {
            var taskId = data.task_id;
            loadingModal.show();
            taskStatus.textContent = "Running Ansible playbook...";
            taskOutput.textContent = "";
            progressBar.style.width = "0%";
            progressBar.textContent = "0%";

            var checkTaskStatus = setInterval(function () {
                fetch('/task_status/' + taskId).then(function (response) {
                    return response.json();
                }).then(function (data) {
                    if (data.state === 'SUCCESS') {
                        clearInterval(checkTaskStatus);
                        taskStatus.textContent = "Playbook completed successfully!";
                        progressBar.style.width = "100%";
                        progressBar.textContent = "100%";
                        taskOutput.textContent += "All tasks completed successfully.\n";
                        loadingModal.hide();
                    } else if (data.state === 'PROGRESS') {
                        taskStatus.textContent = "Running...";
                        var output = data.info.output;
                        var progress = data.info.progress;
                        taskOutput.textContent += output + "\n";
                        progressBar.style.width = progress + "%";
                        progressBar.textContent = progress + "%";
                    } else if (data.state === 'FAILURE') {
                        clearInterval(checkTaskStatus);
                        taskStatus.textContent = "Playbook failed.";
                        loadingModal.hide();
                    }
                });
            }, 1000);
        });
    });
});
