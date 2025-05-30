import * as net from 'net';

const socketPath = '/tmp/socket_file';
const client = net.createConnection(socketPath,() =>{
    console.log('UNIXソケットに接続しました');

    // ソケットにデータを送信
    client.write('');
});

// データを受信したときの処理
client.on('data',(data) => {

    // 必要に応じて接続を終了する
    client.end();
});

// エラーが発声したときの処理
client.on('error',(err) => {
    console.error('エラーが発声しました：',err);
});

// 接続が終了したときの処理
client.on('end',() => {
    console.log('接続が終了しました');
});
