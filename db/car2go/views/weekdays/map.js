function(doc) {
    week=Array(7);
    wday=new Date(doc.Rent.replace(" ","T")).getDay();
    week[wday]=1; 
    emit(wday, week);
}