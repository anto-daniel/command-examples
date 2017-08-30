{
    inputPath="";
    inputFile="";
    if (index($0, "inputPath=") > 0) {
        out = substr($0, index($0,"inputPath="));
        n=split(out,array,",");
        if(n>0)
        {
            inputPath=array[1];
            inputPath=substr(inputPath,17);
        }
    }
    if (index($0, "inputFile=") > 0) {
        out = substr($0, index($0,"inputFile="));
        n=split(out,array,",");
        if(n>0)
        {
            inputFile=array[1];
            inputFile=substr(inputFile,11);

        }
    }
    if(length(inputPath) && length(inputFile) > 0)
        printf("%s %s\n", inputPath, inputFile);
}
