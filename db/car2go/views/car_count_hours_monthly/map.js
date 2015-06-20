function(doc) {
     if (doc.CarId)
	{
	    rt = new Date(doc.Return.replace(" ","T"))
	    rent = new Date(doc.Rent.replace(" ","T"))
	    h=(rt - rent)/1000/3600; 
	    obj = {carid: doc.CarId,
		   month: rent.getMonth(),
		   hours: h
		  };
	    emit(doc.CarId, obj);
	} 
}