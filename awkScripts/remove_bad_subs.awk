BEGIN{
    while ((getline < "badsubs")>0) {
	bad[substr($1,1,6)]=1;
    }
}

!(substr($1,1,6) in bad){print}