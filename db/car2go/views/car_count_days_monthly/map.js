function(doc) {
    if (doc.CarId)
	{
	    rentM = new Date(doc.Rent.replace(" ","T")).getMonth();
	    returnM = new Date(doc.Return.replace(" ","T")).getMonth();
	    emit(doc.CarId, {carid:doc.CarId,
			     month:rentM
			    } );
	    if ( rentM != returnM )
		{
		    emit(doc.CarId, {carid:doc.CarId,
				     month:returnM
			       });
		}

	}
}