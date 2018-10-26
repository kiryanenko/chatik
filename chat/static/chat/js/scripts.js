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


function connectToChat(chat_id) {
    let protocol = window.location.protocol === "http:"? "ws" : 'wss';

    const ws = new WebSocket(protocol + '://' + window.location.host + '/chats/' + chat_id + '/');

    ws.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);

        switch (data.type) {
            case 'new_message':
                add_new_message(data);
                break;
            case 'user_has_read':
                 has_read_chat();
                 break;
        }
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

const BASE_MSG_CLASSES = 'list-group-item list-group-item-action d-flex justify-content-start align-items-center';
const NOT_READ_MSG_CLASS = "list-group-item-light";

function add_new_message(msg) {
    let message = msg.message.replace(/\n/gi, '<br/>');

    let chat = document.getElementById('chat_massages');

    let messageElement = document.createElement('div');
    messageElement.className = BASE_MSG_CLASSES;
    if (!msg.has_read) {
        messageElement.className += ' ' + NOT_READ_MSG_CLASS;
    }
    messageElement.innerHTML = '<img src="/static/chat/images/profile.png" class="mr-3 bg-primary">'
        + '<div class="w-100"><div class="d-flex w-100 justify-content-between">'
        + '<span class="font-weight-bold">' + msg.author + '</span>'
        + '<small>' + msg.created_at + '</small></div>'
        + '<span>' + message + '</span></div>';

    chat.appendChild(messageElement);

    scrollDownMessageBox()
}

function scrollDownMessageBox() {
    let scrollBox = document.getElementsByClassName('message-box')[0];
    scrollBox.scrollTop = scrollBox.scrollHeight;
}

function has_read_chat() {
    let chat = document.getElementById('chat_massages');
    let messages = Array.from(chat.getElementsByClassName(NOT_READ_MSG_CLASS));
    console.log(messages);
    messages.forEach((msg) => msg.className = BASE_MSG_CLASSES)
}
