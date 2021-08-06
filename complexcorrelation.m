%%geotif senslope and mk test
clear;
clc;
%parpool('local');
temppath = 'D:\wangyc\fpar\climatedata\zhuanhuan\temp\';
prepath = 'D:\wangyc\fpar\climatedata\zhuanhuan\pre\';
fparpath = 'D:\wangyc\fpar\2001-2016\tif_mean\';
tempfilelist = dir(strcat(temppath,'*mask.tif'));
prefilelist = dir(strcat(prepath,'*mask.tif'));
fparfilelist = dir(strcat(fparpath,'*.tif'));
n = length(tempfilelist);
temparray = zeros(5310,5429,16);
prearray = zeros(5310,5429,16);
fpararray = zeros(5310,5429,16);
info = geotiffinfo(strcat(fparpath,fparfilelist(1).name));
for i=1:n
    tempfilename = strcat(temppath,tempfilelist(i).name);
    prefilename = strcat(prepath,prefilelist(i).name);
    fparfilename = strcat(fparpath,fparfilelist(i).name);
    temparray(1:4623,1:5429,i) = geotiffread(tempfilename);
    prearray(1:4623,1:5429,i) = geotiffread(prefilename);
    if i == 16
        fpararray(1:5309,1:5216,i) = geotiffread(fparfilename);
    else
        fpararray(1:5310,1:5216,i) = geotiffread(fparfilename);
    end
end
%delete(gcp('nocreate'));
result = zeros(5310,5429,8);
for j=1:5310
    for k=1:5429
        corr_tf = corr2(temparray(i,j,:),fpararray(i,j,:));
        corr_pf = corr2(prearray(i,j,:),fpararray(i,j,:));
        partc_tf_p = partialcorr(temparray(i,j,:),fpararray(i,j,:),prearray(i,j,:));
        partc_pf_t = partialcorr(prearray(i,j,:),fpararray(i,j,:),temparray(i,j,:));
        T_tf_p = partc_tf_p / sqrt(1-partc_tf_p^2) * sqrt(15-1-1);
        T_pf_t = partc_pf_t / sqrt(1-parct_pf_t^2) * sqrt(15-1-1);
        C_f_tp = sqrt(1-(1-corr_tf^2)*(1-parc_pf_t^2));
        F = C_f_tp^2 / (1-C_f_tp^2) * (15-2-1);
        result(i,j,1) = corr_tf;
        result(i,j,2) = corr_pf;
        result(i,j,3) = partc_tf_p;
        result(i,j,4) = partc_pf_t;
        result(i,j,5) = T_tf_p;
        result(i,j,6) = T_pf_t;
        result(i,j,7) = C_f_tp;
        result(i,j,8) = F;
    end
end
save('result.mat','result');
geotiffwrite('R_tf.tif',result(:,:,1),info.SpatialRef,'GeoKeyDirectoryTag',info.GeoTIFFTags.GeoKeyDirectoryTag);
geotiffwrite('R_pf.tif',result(:,:,2),info.SpatialRef,'GeoKeyDirectoryTag',info.GeoTIFFTags.GeoKeyDirectoryTag);
geotiffwrite('PR_tf-p.tif',result(:,:,3),info.SpatialRef,'GeoKeyDirectoryTag',info.GeoTIFFTags.GeoKeyDirectoryTag);
geotiffwrite('PR_pf-t.tif',result(:,:,4),info.SpatialRef,'GeoKeyDirectoryTag',info.GeoTIFFTags.GeoKeyDirectoryTag);
geotiffwrite('T_tf-p.tif',result(:,:,5),info.SpatialRef,'GeoKeyDirectoryTag',info.GeoTIFFTags.GeoKeyDirectoryTag);
geotiffwrite('T_pf-t.tif',result(:,:,6),info.SpatialRef,'GeoKeyDirectoryTag',info.GeoTIFFTags.GeoKeyDirectoryTag);
geotiffwrite('CR_f-tp.tif',result(:,:,7),info.SpatialRef,'GeoKeyDirectoryTag',info.GeoTIFFTags.GeoKeyDirectoryTag);
geotiffwrite('CR-F.tif',result(:,:,8),info.SpatialRef,'GeoKeyDirectoryTag',info.GeoTIFFTags.GeoKeyDirectoryTag);
