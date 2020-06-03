

document.addEventListener('DOMContentLoaded', () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    // When connected, configure button
    socket.on('connect', () => {
        // Notify the server user has joined
          socket.emit('joined');
        // Forget user's last channel when clicked on '+ Channel'
        document.querySelector('#newChannel').addEventListener('click', () => {
            localStorage.removeItem('last_channel');
        });
        // When user leaves channel redirect to '/'
        document.querySelector('#leave').addEventListener('click', () => {
            // Notify the server user has left
            socket.emit('left');
            localStorage.removeItem('last_channel');
            window.location.replace('/');
        })
        // Forget user's last channel when logged out
        document.querySelector('#logout').addEventListener('click', () => {
            localStorage.removeItem('last_channel');
        });

        validInput('#send-button', '#comment');
        document.querySelector('#comment').addEventListener("keydown", event => {

            if (event.key == "Enter") {
                document.getElementById("send-button").click();
            }
        });
        // emits a "message sent" event
        document.querySelector('#send-button').addEventListener("click", () => {
          //Prevent empty inputs being existent
            validInput('#send-button', '#comment');
            let timestamp = new Date;
            timestamp = timestamp.toLocaleTimeString();
            let msg = document.getElementById("comment").value;

            socket.emit('send message', msg, timestamp);
          document.getElementById("comment").value = '';
        });
      });

    // When user joins a channel, add a message  users connected.
    socket.on('status', data => {
              // message of joined user.
        let row ='<' + `${data.msg}` + '>'
        document.getElementById('chat').value += row + '\n';
        // Save user current channel on localStorage
        localStorage.setItem('last_channel', data.channel)
    })
    function validInput(button, input) {
           // Disables submit button by default
           document.querySelector(button).disabled = true;
           // Enables submit button only if user typed something on display name input field
           document.querySelector(input).onclick = () => {
               if (document.querySelector(input).value.length > 0) {
                   document.querySelector(button).disabled = false;
               } else {
                   document.querySelector(button).disabled = true;
               }

           }
       }

    // When a message is announced, add it to the textarea.
    socket.on('announce message', data => {
        // Format message
        let row = '<' + `${data.timestamp}` + '> - ' + '[' + `${data.user}` + ']:  ' + `${data.msg}`
        document.querySelector('#chat').value += row + '\n'
    })

    document.addEventListener('click', () => {
    const h1 = document.querySelector('h1');
    h1.style.animationPlayState  = 'paused';
    document.querySelector('button').onclick = () => {
        if (h1.style.animationPlayState  === 'paused')
            h1.style.animationPlayState = 'running, running';
        else
            h1.style.animationPlayState  = 'paused';
    };
  });
});
