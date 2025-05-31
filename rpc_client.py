import * as net from 'net';
import { v4 as uuidv4 }  from 'uuid';

const method = process.argv[2];

if (!method){
    console.error("関数名を指定してください。");
    process.exit(1);
}

let functionArgs = [];

if(method == "sort"){
    const argString = process.argv[3];
    if(typeof argString !== 'string' || argString.length === 0){
        console.error("エラー：sort関数にはカンマ区切りの文字列引数を一つ指定してください。")
        process.exit(1);
    }

    functionArgs = argString.split(',');
}else{
    const rawArgs = process.argv.slice(3);
    functionArgs = rawArgs.map(arg => {
        const num = Number(arg);
        if(!isNaN(num) && arg.trim() !== ''){
            return num;
        }
        return arg;
    });
}

const paramTypes = functionArgs.map(arg => typeof arg);

const uniqueId = uuidv4();

const message = {
    method_name : method,
    arguments: functionArgs,
    param_type : paramTypes,
    id : uniqueId
};


const socketPath = '/tmp/socket_file';
const client = net.createConnection(socketPath,() =>{
    console.log('UNIXソケットに接続しました');

    // ソケットにデータを送信
    client.write(JSON.stringify(message));
});

// データを受信したときの処理
client.on('data',(data) => {

    // 必要に応じて接続を終了する
    const response = JSON.parse(data.toString());
    console.log('',response);
    client.end();
});

// エラーが発声したときの処理
client.on('error',(err) => {
    console.error('エラーが発生しました：',err);
});

// 接続が終了したときの処理
client.on('end',() => {
    console.log('接続が終了しました');
});
