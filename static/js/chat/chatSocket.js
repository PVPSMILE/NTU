$(document).ready(function(e) {
    const roomName = JSON.parse(document.getElementById('room-name').textContent);
    const yourName = JSON.parse(document.getElementById('Name').textContent);
    const yourSurname = JSON.parse(document.getElementById('Surname').textContent);
    const yourEmail =  JSON.parse(document.getElementById('Email').textContent);
    const friendEmail =  JSON.parse(document.getElementById('friend').textContent);
    var chatSocket;
    var NotificationSocket;
    var messageBody = document.querySelector('#chat2');
    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
    function connect(){
            console.log("chatSocket connect");
            chatSocket = new WebSocket(
                'ws://'
                + window.location.host
                + '/ws/chat/'
                + roomName
                + '/'
            );
            chatSocket.onopen = function(e){
                chatSocket.send(JSON.stringify({
                    "status": "connect",
                    'name': yourName, 
                    'room_name': roomName,
                    'email': yourEmail,
                }));
            }
            chatSocket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                var request = data.message;
                console.log(request);
                if (request.status == "send"){
                    var date = new Date();
                    var currenttime = ((date.getHours() < 10)?"0":"") + date.getHours() + ":"  + ((date.getMinutes() < 10)?"0":"")+ date.getMinutes();
                    if (request.email == yourEmail){
                        document.querySelector("#chat2").insertAdjacentHTML('beforeend', `
                        <li class="d-flex justify-content-between mb-4">
                            <div class="card w-100">
                                <div class="card-header d-flex justify-content-between p-3">
                                    <p class="fw-bold mb-0">You</p>
                                    <p class="text-muted small mb-0"><i class="far fa-clock"></i>${request.time}</p>
                                </div>
                                <div class="card-body">
                                    <p class="mb-0">
                                        ${request.message}
                                    </p>
                                </div>
                            </div>
                            <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-5.webp" alt="avatar"
                                    class="rounded-circle d-flex align-self-start ms-3 shadow-1-strong" width="60">
                        </li>`);
                        var messageBody = document.querySelector('#chat2');
                        messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
                    
                    }
                    else{
                        document.querySelector("#chat2").insertAdjacentHTML('beforeend', `
                        <li class="d-flex justify-content-between mb-4">
                            <div class="card w-100">
                                <div class="card-header d-flex justify-content-between p-3">
                                    <p class="fw-bold mb-0">${request.name}</p>
                                    <p class="text-muted small mb-0"><i class="far fa-clock"></i>${currenttime}</p>
                                </div>
                                <div class="card-body">
                                    <p class="mb-0">
                                        ${request.message}
                                    </p>
                                </div>
                            </div>
                            <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-5.webp" alt="avatar"
                                    class="rounded-circle d-flex align-self-start ms-3 shadow-1-strong" width="60">
                        </li>`);
                        var messageBody = document.querySelector('#chat2');
                        messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
                    }

            }
            
        };
        chatSocket.onclose = function(e) {
            console.error('ChatSocketsocket closed unexpectedly');
            setTimeout(connect,1000);
        };
        chatSocket.onerror = function(err) {
            chatSocket.error('chatSocket encountered error: ', err.message, 'Closing socket');
            chatSocket.close();
        };
    }
    function connect2(){
        console.log("NotificationSocket connect");
        NotificationSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chats/'
        );
        NotificationSocket.onopen = function(e){
            NotificationSocket.send(JSON.stringify({
                    "status": "connect",
                    'name': yourName, 
                    'room_name': roomName,
                    'email': yourEmail,
                }));
        }
        NotificationSocket.onmessage = function(e){
            const data = JSON.parse(e.data);
            var request = data.message;
            console.log(request);
            if (request.status == "send"){
                NotificationSocket.send(JSON.stringify({
                    'status': "check",
                    'message': request.message, 
                    'name': request.name,
                    'room_name': request.room_name,
                }));

            }
            else if (request.status == "add_message_note"){
                $(".room").each(function (indexInArray) { 
                    if ($(this).text()==request.room_name){
                        console.log($(this).text()); 
                        $(this).siblings(".last_message").text(request.message);
                    }
                });

            }
            else if (request.status == "add_chat"){
                var url_mask = "/chat/room_name/".replace("room_name", request.room_name);
                document.querySelector("#chat").insertAdjacentHTML('beforeend', `
                <li class="p-2 border-bottom q">
                <a href="#!" class="d-flex justify-content-between chat">
                    <div class="d-flex flex-row chats">
                        <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-8.webp" alt="avatar" class="rounded-circle d-flex align-self-center me-3 shadow-1-strong" width="60">
                        <div class="email pt-1">
                            <a href=${url_mask}><p class="fw-bold mb-0">${request.surname} ${request.name}</p></a>
                            <p class="room" style="display: none;">${request.room_name}</p>
                            <p class="small text-muted">${request.message}</p>
                        </div>
                    </div>
                    <!-- <div class="pt-1">
                    <p class="small text-muted mb-1">Just now</p>
                    <span class="badge bg-danger float-end">1</span>
                    </div> -->
                </a>
                </li>`);
            }
            else if(request.status == "get_chat"){   
                $('.q').each(function(){
                    $(this).remove(); 
                });
                var list_chats = request.rooms;
                var list_last_messages = request.last_messages;
                for (var index = 0; index < list_chats.length; index++) {
                    var element = list_chats[index];
                    var last_message;
                    for (var i = 0; index < list_last_messages.length; i++) {
                        var message = list_last_messages[i];
                        if (message.room_name==element.room_name){
                            last_message = message.message;
                        }
                    }
                    var url_mask = "/chat/room_name/".replace("room_name", element.room_name);
                    document.querySelector("#chat").insertAdjacentHTML('beforeend', `
                        <li class="p-2 border-bottom q">
                        <a href="#!" class="d-flex justify-content-between chat">
                            <div class="d-flex flex-row chats">
                                <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-8.webp" alt="avatar" class="rounded-circle d-flex align-self-center me-3 shadow-1-strong" width="60">
                                <div class="email pt-1">
                                    <a href=${url_mask}><p class="fw-bold mb-0">${element.surname} ${element.name}</p></a>
                                    <p class="room" style="display: none;">${element.room_name}</p>
                                    <p class="small text-muted last_message">${last_message}</p>
                                </div>
                            </div>
                            <!-- <div class="pt-1">
                            <p class="small text-muted mb-1">Just now</p>
                            <span class="badge bg-danger float-end">1</span>
                            </div> -->
                        </a>
                        </li>`);            
                }

            }
            else if(request.status == "list_chat"){
                $('.q').each(function(){
                    $(this).remove(); 
                });
                var list_chats = request.rooms;
                var list_last_messages = request.last_messages;
                for (var index = 0; index < list_chats.length; index++) {
                    var element = list_chats[index];
                    var last_message;
                    for (var i = 0; index < list_last_messages.length; i++) {
                        var message = list_last_messages[i];
                        if (message.room_name==element.room_name){
                            last_message = message.message;
                        }
                    }
                    var url_mask = "/chat/room_name/".replace("room_name", element.room_name);
                    document.querySelector("#chat").insertAdjacentHTML('beforeend', `
                        <li class="p-2 border-bottom q">
                        <a href="#!" class="d-flex justify-content-between chat">
                            <div class="d-flex flex-row chats">
                                <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-8.webp" alt="avatar" class="rounded-circle d-flex align-self-center me-3 shadow-1-strong" width="60">
                                <div class="email pt-1">
                                    <a href=${url_mask}><p class="fw-bold mb-0">${element.surname} ${element.name}</p></a>
                                    <p class="room" style="display: none;">${element.room_name}</p>
                                    <p class="small text-muted last_message">${last_message}</p>
                                </div>
                            </div>
                            <!-- <div class="pt-1">
                            <p class="small text-muted mb-1">Just now</p>
                            <span class="badge bg-danger float-end">1</span>
                            </div> -->
                        </a>
                        </li>`);            
                }
            }
            else if(request.status == "get_friend"){
                $('.h').each(function(){
                    $(this).remove(); 
                });
                var list_friends = request.friends;
                for (var index = 0; index < list_friends.length; index++) {
                    var element = list_friends[index];
                    document.querySelector("#chat3").insertAdjacentHTML('beforeend', `
                        <li class="p-2 border-bottom h">
                        <a href="#!" class="d-flex justify-content-between chat">
                            <div class="d-flex flex-row chats">
                                <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-8.webp" alt="avatar" class="rounded-circle d-flex align-self-center me-3 shadow-1-strong" width="60">
                                <div class="email pt-1">
                                    <p class="fw-bold mb-0">${element.surname} ${element.name}</p>
                                </div>
                            </div>
                        </a>
                        </li>
                    `);            
                }

            }
            else if(request.status == "list_friend"){
                $('.h').each(function(){
                    $(this).remove(); 
                });
                var list_friends = request.friends;
                for (var index = 0; index < list_friends.length; index++) {
                    var element = list_friends[index];
                    document.querySelector("#chat3").insertAdjacentHTML('beforeend', `
                        <li class="p-2 border-bottom h">
                        <a href="#!" class="d-flex justify-content-between chat">
                            <div class="d-flex flex-row chats">
                                <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-8.webp" alt="avatar" class="rounded-circle d-flex align-self-center me-3 shadow-1-strong" width="60">
                                <div class="email pt-1">
                                    <p class="fw-bold mb-0">${element.surname} ${element.name}</p>
                                </div>
                            </div>
                        </a>
                        </li>
                    `);           
                }
            }
        };
        NotificationSocket.onclose = function(e) {
            console.error('Notificationsocket closed unexpectedly');
            setTimeout(connect2,1000);
       };
       NotificationSocket.onerror = function(err) {
            NotificationSocket.error('NotificationSocket encountered error: ', err.message, 'Closing socket');
            NotificationSocket.close();
        };
    }
    connect();
    connect2();
    document.querySelector('#send').focus();
    document.querySelector('#send').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#send').click();
        }
    };
    document.querySelector('#send').onclick = function(e) {
        const messageInputDom = document.querySelector('#textAreaExample2');
        const message = messageInputDom.value;
        // const email = 
        // document.querySelector("#chat2").insertAdjacentHTML('beforeend', `
        // <li class="d-flex justify-content-between mb-4">
        //     <div class="card w-100">
        //         <div class="card-header d-flex justify-content-between p-3">
        //             <p class="fw-bold mb-0">Lara Croft</p>
        //             <p class="text-muted small mb-0"><i class="far fa-clock"></i> 13 mins ago</p>
        //         </div>
        //         <div class="card-body">
        //             <p class="mb-0">
        //                 ${message}
        //             </p>
        //         </div>
        //     </div>
        //     <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-5.webp" alt="avatar"
        //             class="rounded-circle d-flex align-self-start ms-3 shadow-1-strong" width="60">
        // </li>`);
        var date = new Date(); 
        // var currenttimesecond = date.getHours() + ":"  + date.getMinutes() + ":" + date.getSeconds();
        var currenttime = ((date.getHours() < 10)?"0":"") + date.getHours() + ":"  + ((date.getMinutes() < 10)?"0":"")+ date.getMinutes();
        chatSocket.send(JSON.stringify({
            'status': "send",
            'message': message,
            'name': yourName, 
            'surname': yourSurname,
            'room_name': roomName,
            'email': yourEmail,
            'time': currenttime,
        }));
        messageInputDom.value = '';
    };
    $("#add").click(function (e) { 
        chatSocket.send(JSON.stringify({
            'status': "add_friend",
            'name': yourName, 
            'room_name': roomName,
            'email': yourEmail,
            'friend_email': friendEmail,
        }));
        $("#list").remove();
        
    });
    $("#search").click(function (e) { 
        $("#search").keyup(function (e) {
            if(String($("#search").val()).length>0){
                NotificationSocket.send(JSON.stringify({
                    'status': "search_chat",
                    'value': $("#search").val(), 
                    'name': yourName,
                    'email': yourEmail,
                    'surname': yourSurname,
                }));
            }
            else{
                NotificationSocket.send(JSON.stringify({
                    'status': "get_list_chats",
                    'name': yourName,
                    'email': yourEmail,
                    'surname': yourSurname,
                })); 
            }
        });
        
    });
    $("#search_friend").click(function (e) { 
        $("#search_friend").keyup(function (e) {
            if(String($("#search_friend").val()).length>0){
                NotificationSocket.send(JSON.stringify({
                    'status': "search_friend",
                    'value': $("#search_friend").val(), 
                    'name': yourName,
                    'email': yourEmail,
                    'surname': yourSurname,
                }));
            }
            else{
                NotificationSocket.send(JSON.stringify({
                    'status': "get_list_friends",
                    'name': yourName,
                    'email': yourEmail,
                    'surname': yourSurname,
                })); 
            }
        });
        
    });
});