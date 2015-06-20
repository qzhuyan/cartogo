function(keys, values, rereduce) {
    if (! rereduce) {
	cars_monthly = {};
	for (i=0; i<values.length; i++)
	{
	    key = values[i].carid;
	    m = values[i].month;
	    if ( !cars_monthly[key] )
	    {
		yearm = Array(12);
		yearm[m] = 1;
		cars_monthly[key] = yearm;
	    }
	    else {
		if (cars_monthly[key][m])
		    cars_monthly[key][m] += 1; 
		else
		    cars_monthly[key][m] = 1;
	    }
	    
	}
	

	var res = {};
	for (var car in cars_monthly)
    	{
    	    m = cars_monthly[car];

    	    total = 0;
	    
    	    for(i=0;i<12;i++)
		if (m[i])
    		    total += m[i];

    	    res[car] = 
    	    	{
    	    	    sum: total,
    	    	    permonth: m
    	    	};
    	}
	
	return res; //{carid1: {res: total, permonth: {Jan,Feb,Mar,...Dec}}, {carid2...}, ... }
    }
    else // rereduce
	{
	    res = {};
	    for (i=0; i<values.length; i++) //iterate reduce res value
	    {
		reduce_res = values[i]; 
		for(n in reduce_res)    //iterate car in reduce res
		{
		    if ( ! res[n] ) // Fist showup
			res[n] = reduce_res[n];
		    else
		    { // append 
			res[n].sum += reduce_res[n].sum;
			for (x=0; x<12; x++)
			    res[n].permonth[x] += reduce_res[n].permonth[x];    
			
		    }
		}

	    }

	    return res;
	}

}