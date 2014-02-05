function upload(){
 scp $1 guxxx220@98.143.37.111:~/capstone
}

function download(){
 scp guxxx220@98.143.37.111:~/capstone/$1 ~/Capstone
}
