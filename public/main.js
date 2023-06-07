const sio = io();

sio.on('connect', () => {
    console.log('connected');
});


sio.on('disconnect', () => {
    console.log('disconnected');
});

sio.emit('create or join', { 'room': 'room_1' });

sio.on('created', (data) => {
    console.log('Created Room' + data['room'])
})

sio.on('user_count', (data) => {
    console.log('There are ' + data['client_count'] + ' clients in room: ' + data['room']);
});

sio.on('room_count', (data) => {
    console.log('There are ' + data['client_count'] + ' clients in this room');
})

sio.on('join', (data) => {
    console.log('Another peer made a request to join room: ' + data['room']);
})

sio.on('joined', (data) => {
    console.log(data['sid'] + ' joined ' + data['room']);
})

sio.emit('message', 'Lorem Ipsum blah blah');

sio.on('full', (data) => {
    console.log('Room ' + data['room'] + ' is full')
})

sio.on('message', (message) => {
    console.log(message);
});

sio.on('bye', (data) => {
    console.log(data['sid'] + " left the room.");
})