"use strict";


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


function sendMessage(chat, msg) {
    $.ajax({
        url: '/chats/' + chat + '/messages/',
        type: 'POST',
        data: { message: msg, csrfmiddlewaretoken: csrftoken },
        success: function(data) {
            addNewMessage(data)
        }
    })
}


let ws;

function connectToChat(chat_id) {
    let protocol = window.location.protocol === "http:"? "ws" : 'wss';

    ws = new WebSocket(protocol + '://' + window.location.host + '/chats/' + chat_id + '/');

    ws.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);

        switch (data.type) {
            case 'new_message':
                addNewMessage(data.data);
                sendHasReadChat();
                break;
            case 'user_has_read':
                userHasReadChat();
                break;
        }
    };

    ws.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
}

function sendHasReadChat() {
    ws.send(JSON.stringify({
        'type': 'has_read'
    }))
}


const BASE_MSG_CLASSES = 'list-group-item list-group-item-action d-flex align-items-start';
const NOT_READ_MSG_CLASS = "list-group-item-light";

function addNewMessage(msg) {
    let message = msg.message.replace(/\n/gi, '<br/>');

    let chat = document.getElementById('chat_massages');

    let messageElement = document.createElement('div');
    messageElement.className = BASE_MSG_CLASSES;
    if (!msg.has_read) {
        messageElement.className += ' ' + NOT_READ_MSG_CLASS;
    }
    messageElement.innerHTML = '<img src="/static/chat/images/profile.png" class="mr-3 mt-2 bg-primary">'
        + '<div class="w-100"><div class="d-flex w-100 justify-content-between">'
        + '<div class="row">'
        + '<span class="col font-weight-bold">' + msg.author + '</span>'
        + '<small class="col-auto">' + msg.created_at + '</small></div>'
        + '</div>'
        + '<span>' + message + '</span></div>';

    chat.appendChild(messageElement);

    scrollDownMessageBox()
}

function scrollDownMessageBox() {
    let scrollBox = document.getElementsByClassName('message-box')[0];
    scrollBox.scrollTop = scrollBox.scrollHeight;
}

function userHasReadChat() {
    let chat = document.getElementById('chat_massages');
    let messages = Array.from(chat.getElementsByClassName(NOT_READ_MSG_CLASS));
    messages.forEach((msg) => msg.className = BASE_MSG_CLASSES)
}
