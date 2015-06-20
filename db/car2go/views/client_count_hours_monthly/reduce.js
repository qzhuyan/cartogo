function(keys, values, rereduce) {
    if (! rereduce) {
	clients_monthly = {};
	for (i=0; i<values.length; i++)
	{
	    key = values[i].clientid;
	    m = values[i].month;
	    h = values[i].hours;
	    if ( !clients_monthly[key] )
	    {
		yearm = Array(12);
		yearm[m] = h;
		clients_monthly[key] = yearm;
	    }
	    else {
		if (clients_monthly[key][m])
		    clients_monthly[key][m] += h; 
		else
		    clients_monthly[key][m] = h;
	    }
	    
	}
	

	var res = {};
	for (var client in clients_monthly)
    	{
    	    m = clients_monthly[client];

    	    total = 0;
	    
    	    for(i=0;i<12;i++)
		if (m[i])
    		    total += m[i];

    	    res[client] = 
    	    	{
    	    	    sum: total,
    	    	    permonth: m
    	    	};
    	}
	
	return res; //{clientid1: {res: total, permonth: {Jan,Feb,Mar,...Dec}}, {clientid2...}, ... }
    }
    else // rereduce
	{
	    res = {};
	    for (i=0; i<values.length; i++) //iterate reduce res value
	    {
		reduce_res = values[i]; 
		for(n in reduce_res)    //iterate client in reduce res
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