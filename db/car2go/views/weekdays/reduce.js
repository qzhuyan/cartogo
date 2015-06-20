function(keys, values,rereduce) {

    week=[0,0,0,0,0,0,0]; 

    if (rereduce) 
    {
	for(i=0; i<values.length;i++)
	{
	    for(y=0; y<7; y++) 
	    { 
		week[y] += values[i][y];
	    }
	}
	return week;
    }
    else {

	for(index=0; index<values.length;index++ ) 
	{ for(y=0; y<7; y++) 
	  { 
	      week[y] += values[index][y];
	  }
	}; 
	return week; 
    }
}