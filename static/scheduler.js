document.addEventListener('DOMContentLoaded', function() {
    restoreTasks();
});

document.getElementById('scheduleForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const taskName = document.getElementById('taskName').value;
    const taskTime = document.getElementById('taskTime').value;
    const taskColor = document.getElementById('taskColor').value;
    const task = { taskName, taskTime, taskColor };
    addTask(task);
    saveTask(task);
});

function saveTask(task) {
    let tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    tasks.push(task);
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function restoreTasks() {
    const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    tasks.forEach(task => addTask(task));
}

function addTask(task) {
    const { taskName, taskTime, taskColor } = task;
    const li = document.createElement('li');
    li.style.backgroundColor = taskColor;
    li.style.display = 'flex';
    li.style.justifyContent = 'space-between';
    li.style.alignItems = 'center';
    li.style.flexWrap = 'wrap'; // 2行に折り返す

    const taskDetails = document.createElement('div');
    taskDetails.style.flexBasis = '100%'; // 全幅を取る

    const timeDisplay = document.createElement('span');
    timeDisplay.textContent = `${taskName} - ${taskTime} `;
    taskDetails.appendChild(timeDisplay);

    const timerDisplay = document.createElement('div');
    taskDetails.appendChild(timerDisplay);

    li.appendChild(taskDetails);

    const deleteButton = document.createElement('button');
    deleteButton.textContent = '削除';
    deleteButton.style.marginLeft = 'auto'; // 右端に配置
    deleteButton.style.order = 2; // 他の要素より後に表示
    deleteButton.style.padding = '4px 8px';
    deleteButton.style.fontSize = '0.8rem';
    deleteButton.onclick = function() {
        li.remove();
        removeTask(task);
    };

    li.appendChild(deleteButton);

    document.getElementById('taskList').appendChild(li);
    scheduleAlarm(taskName, taskTime, timerDisplay);
}

function removeTask(taskToRemove) {
    let tasks = JSON.parse(localStorage.getItem('tasks')) || [];
    tasks = tasks.filter(task => task.taskTime !== taskToRemove.taskTime);
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

function scheduleAlarm(taskName, taskTime, timerDisplay) {
    const now = new Date();
    const scheduledTime = new Date(taskTime);  // 'taskTime'は`datetime-local`からの完全な日付と時刻を含む
    const timeout = scheduledTime - now;

    if (timeout < 0) {
        timerDisplay.textContent = "設定された時間は過去のものです";
        return;  // 過去の日時にタイマーをセットしないように処理を終了
    }

    let interval = setInterval(function() {
        const secondsLeft = Math.round((scheduledTime - new Date()) / 1000);
        if (secondsLeft > 0) {
            const hours = Math.floor(secondsLeft / 3600);
            const minutes = Math.floor((secondsLeft % 3600) / 60);
            const seconds = secondsLeft % 60;
            timerDisplay.textContent = `残り時間: ${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        } else {
            timerDisplay.textContent = "時間です！";
            clearInterval(interval);
            playAlarm();
        }
    }, 1000);
}

function playAlarm() {
    const alarmSound = document.getElementById('alarmSound');
    alarmSound.play();
    setTimeout(() => alarmSound.pause(), 30000); // 30秒後に音楽を停止
}
