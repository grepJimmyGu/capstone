function dl(){
    grep href\= ~/Capstone/data|cut -d'"' -f4|grep \.csv|cut -d'/' -f7 > filename
    name=$(grep href\= ~/Capstone/data|cut -d'"' -f4|grep \.csv|cut -d'/' -f7)
    for i in $name 
    do curl -O -k https://raw2.github.com/umbrae/reddit-top-2.5-million/master/data/$i
       echo "You Have downloaded "$i
    done
}
