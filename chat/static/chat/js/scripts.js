function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


function connectToChat(chat_id) {
    let protocol = window.location.protocol === "http:"? "ws" : 'wss';

    const ws = new WebSocket(protocol + '://' + window.location.host + '/chats/' + chat_id + '/');

    ws.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);

        add_new_message(data)
    };

    ws.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
}


function sendMessage(chat, msg) {
    $.ajax({
        url: '/chats/' + chat + '/messages/',
        type: 'POST',
        data: { message: msg, csrfmiddlewaretoken: csrftoken }
    })
}


function add_new_message(msg) {
    let message = msg.message.replace(/\n/gi, '<br/>');

    let messageBox = document.getElementById('chat_massages');

    let messageElement = document.createElement('div');
    messageElement.className = "list-group-item list-group-item-action d-flex justify-content-start align-items-center";
    messageElement.innerHTML = '<img src="/static/chat/images/profile.png" class="mr-3 bg-primary">'
        + '<div class="w-100"><div class="d-flex w-100 justify-content-between">'
        + '<span class="font-weight-bold">' + msg.author + '</span>'
        + '<small>' + msg.created_at + '</small></div>'
        + '<span>' + message + '</span></div>';

    messageBox.appendChild(messageElement);

    scrollDownMessageBox()
}

function scrollDownMessageBox() {
    let scrollBox = document.getElementsByClassName('message-box')[0];
    scrollBox.scrollTop = scrollBox.scrollHeight;
}
