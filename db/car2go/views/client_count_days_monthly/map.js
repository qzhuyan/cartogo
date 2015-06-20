function(doc) {
    if (doc.CarId)
    {
	rt = new Date(doc.Return.replace(" ","T"))
	rent = new Date(doc.Rent.replace(" ","T"))
	obj = {clientid: doc.Client,
	       month: rent.getMonth(),
	      };
	emit(doc.client, obj);
    } 
    
}