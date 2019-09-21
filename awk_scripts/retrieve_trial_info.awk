$0~/TRIAL_RESULT 0/ {
    if(subj!="") print subj,item,clash,second,list,target;
    trial=$NF;
}
$(NF-1)=="list" {list=$NF;subj=FILENAME;}
$(NF-1)=="clashtype" {clash=$NF;}
$(NF-1)=="secondarytask" {second=$NF;}
$(NF-1)=="line2target" {target=$NF;}
$(NF-1)=="subtypeid" {item=$NF;}

