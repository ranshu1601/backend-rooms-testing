const sio=io();

sio.on('connect', () =>{
    console.log('connected')
});

sio.on('log', (data) =>{
    console.log(data)
});