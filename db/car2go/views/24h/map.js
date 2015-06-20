function(doc) {
    if (doc.CarId)
    {
	//obj = {date:doc.Rent,weekday:Rent.getDay(),customerName:doc.Client, carId:doc.CarId, hours:hours};

	rt = new Date(doc.Return.replace(" ","T"));
	rent = new Date(doc.Rent.replace(" ","T"));
	hours=(rt - rent)/1000/3600; 
	obj = {date:doc.Rent,
	       weekday:rent.getDay(),
	       customerName:doc.Client, 
	       carId:doc.CarId, 
	       hours:hours};

	emit(doc._id,obj);
    }
}