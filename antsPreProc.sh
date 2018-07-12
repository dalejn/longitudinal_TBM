#!/bin/bash

set -e -x

base=/gpfs/gsfs6/users/Hippo_hr/moa/anal/TBM
wd=/gpfs/gsfs6/users/Hippo_hr/moa/sourcedata/
cd $base

for x in sub-???; do 
    if [ -e $x/*/ses*/anat/lhipp_t2s.nii.gz ];then
	echo $x;fi
done > $wd/subs.txt

cd $wd
rm -f bfcSwrm dilSwrm
for x in `cat subs.txt`;do 
    if [ -e $base/$x/hipp/lhipp_t2s.nii.gz ];then
	ln -sf $base/$x/hipp/lhipp_t2s.nii.gz l${x}-t2s.nii.gz
	ln -sf $base/$x/hipp/lhipp_t1.nii.gz l${x}-t1.nii.gz
	ln -sf $base/$x/hipp/lh.hippoSfLabels-T1-multispecT1T2.v10.nii.gz l${x}-lab.nii.gz
	fslmaths $base/$x/hipp/lh.hippoSfLabels-T1-multispecT1T2.v10.nii.gz -bin l${x}-lab.nii.gz &
	echo	"export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8;$ANTSPATH/N4BiasFieldCorrection -d 3 -b [200] -c [50x50x40x30,0.00000001] -i $wd/l${x}-t2s.nii.gz -o $wd/l${x}-t2s-bfc.nii.gz -r 0 -s 2 --verbose 1"  >> bfcSwrm
	echo	"export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8;$ANTSPATH/N4BiasFieldCorrection -d 3 -b [200] -c [50x50x40x30,0.00000001] -i $wd/l${x}-t1.nii.gz -o $wd/l${x}-t1-bfc.nii.gz -r 0 -s 2 --verbose 1" >> bfcSwrm
	echo "fslmaths  l${x}-lab.nii.gz -dilF -dilF -dilF  l${x}-dil.nii.gz" >> dilSwrm
    fi
done

for x in `cat subs.txt`;do 
    if [ -e $base/$x/hipp/rhipp_t2s.nii.gz ];then
	ln -sf $base/$x/hipp/rhipp_t2s.nii.gz r${x}-t2s.nii.gz
	ln -sf $base/$x/hipp/rhipp_t1.nii.gz r${x}-t1.nii.gz
	ln -sf $base/$x/hipp/rh.hippoSfLabels-T1-multispecT1T2.v10.nii.gz r${x}-lab.nii.gz
	fslmaths $base/$x/hipp/rh.hippoSfLabels-T1-multispecT1T2.v10.nii.gz -bin r${x}-lab.nii.gz &
	echo	"export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8;$ANTSPATH/N4BiasFieldCorrection -d 3 -b [200] -c [50x50x40x30,0.00000001] -i $wd/r${x}-t2s.nii.gz -o $wd/r${x}-t2s-bfc.nii.gz -r 0 -s 2 --verbose 1"  >> bfcSwrm
	echo	"export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8;$ANTSPATH/N4BiasFieldCorrection -d 3 -b [200] -c [50x50x40x30,0.00000001] -i $wd/r${x}-t1.nii.gz -o $wd/r${x}-t1-bfc.nii.gz -r 0 -s 2 --verbose 1" >> bfcSwrm
	echo "fslmaths r${x}-lab.nii.gz -dilF -dilF -dilF r${x}-dil.nii.gz" >> dilSwrm
    fi
done
# d731 is near the center of the group space
# Padding with 55 voxels on all sides
#/data/adamt/build/antsbin/bin/ImageMath 3 padded.nii.gz PadImage d731-t1.nii.gz 55
#/data/adamt/build/antsbin/bin/ImageMath 3 frame.nii.gz m padded.nii.gz 0
#rm -f padded.nii.gz

#/data/adamt/build/antsbin/bin/AverageImages 3 lhtemplate0.nii.gz 1 ld701-lab.nii.gz ld702-lab.nii.gz ld703-lab.nii.gz ld704-lab.nii.gz ld705-lab.nii.gz ld706-lab.nii.gz ld707-lab.nii.gz ld708-lab.nii.gz ld709-lab.nii.gz ld710-lab.nii.gz ld711-lab.nii.gz ld712-lab.nii.gz ld713-lab.nii.gz ld714-lab.nii.gz ld715-lab.nii.gz ld716-lab.nii.gz ld717-lab.nii.gz ld720-lab.nii.gz ld722-lab.nii.gz ld723-lab.nii.gz ld724-lab.nii.gz ld726-lab.nii.gz ld727-lab.nii.gz ld728-lab.nii.gz ld729-lab.nii.gz ld730-lab.nii.gz ld731-lab.nii.gz ld732-lab.nii.gz ld734-lab.nii.gz ld735-lab.nii.gz ld736-lab.nii.gz ld737-lab.nii.gz ld738-lab.nii.gz ld739-lab.nii.gz ld740-lab.nii.gz ld741-lab.nii.gz ld743-lab.nii.gz ld744-lab.nii.gz ld745-lab.nii.gz ld747-lab.nii.gz ld748-lab.nii.gz ld749-lab.nii.gz ld750-lab.nii.gz ld752-lab.nii.gz ld753-lab.nii.gz ld754-lab.nii.gz ld755-lab.nii.gz frame.nii.gz

#/data/adamt/build/antsbin/bin/AverageImages 3 lhtemplate1.nii.gz 1 ld701-t1.nii.gz ld702-t1.nii.gz ld703-t1.nii.gz ld704-t1.nii.gz ld705-t1.nii.gz ld706-t1.nii.gz ld707-t1.nii.gz ld708-t1.nii.gz ld709-t1.nii.gz ld710-t1.nii.gz ld711-t1.nii.gz ld712-t1.nii.gz ld713-t1.nii.gz ld714-t1.nii.gz ld715-t1.nii.gz ld716-t1.nii.gz ld717-t1.nii.gz ld720-t1.nii.gz ld722-t1.nii.gz ld723-t1.nii.gz ld724-t1.nii.gz ld726-t1.nii.gz ld727-t1.nii.gz ld728-t1.nii.gz ld729-t1.nii.gz ld730-t1.nii.gz ld731-t1.nii.gz ld732-t1.nii.gz ld734-t1.nii.gz ld735-t1.nii.gz ld736-t1.nii.gz ld737-t1.nii.gz ld738-t1.nii.gz ld739-t1.nii.gz ld740-t1.nii.gz ld741-t1.nii.gz ld743-t1.nii.gz ld744-t1.nii.gz ld745-t1.nii.gz ld747-t1.nii.gz ld748-t1.nii.gz ld749-t1.nii.gz ld750-t1.nii.gz ld752-t1.nii.gz ld753-t1.nii.gz ld754-t1.nii.gz ld755-t1.nii.gz frame.nii.gz

#/data/adamt/build/antsbin/bin/AverageImages 3 lhtemplate2.nii.gz 1 ld701-t2s.nii.gz ld702-t2s.nii.gz ld703-t2s.nii.gz ld704-t2s.nii.gz ld705-t2s.nii.gz ld706-t2s.nii.gz ld707-t2s.nii.gz ld708-t2s.nii.gz ld709-t2s.nii.gz ld710-t2s.nii.gz ld711-t2s.nii.gz ld712-t2s.nii.gz ld713-t2s.nii.gz ld714-t2s.nii.gz ld715-t2s.nii.gz ld716-t2s.nii.gz ld717-t2s.nii.gz ld720-t2s.nii.gz ld722-t2s.nii.gz ld723-t2s.nii.gz ld724-t2s.nii.gz ld726-t2s.nii.gz ld727-t2s.nii.gz ld728-t2s.nii.gz ld729-t2s.nii.gz ld730-t2s.nii.gz ld731-t2s.nii.gz ld732-t2s.nii.gz ld734-t2s.nii.gz ld735-t2s.nii.gz ld736-t2s.nii.gz ld737-t2s.nii.gz ld738-t2s.nii.gz ld739-t2s.nii.gz ld740-t2s.nii.gz ld741-t2s.nii.gz ld743-t2s.nii.gz ld744-t2s.nii.gz ld745-t2s.nii.gz ld747-t2s.nii.gz ld748-t2s.nii.gz ld749-t2s.nii.gz ld750-t2s.nii.gz ld752-t2s.nii.gz ld753-t2s.nii.gz ld754-t2s.nii.gz ld755-t2s.nii.gz frame.nii.gz

#/data/adamt/build/antsbin/bin/AverageImages 3 rhtemplate0.nii.gz 1 rd701-lab.nii.gz rd702-lab.nii.gz rd703-lab.nii.gz rd704-lab.nii.gz rd705-lab.nii.gz rd706-lab.nii.gz rd707-lab.nii.gz rd708-lab.nii.gz rd709-lab.nii.gz rd710-lab.nii.gz rd711-lab.nii.gz rd712-lab.nii.gz rd713-lab.nii.gz rd714-lab.nii.gz rd715-lab.nii.gz rd716-lab.nii.gz rd717-lab.nii.gz rd720-lab.nii.gz rd722-lab.nii.gz rd723-lab.nii.gz rd724-lab.nii.gz rd726-lab.nii.gz rd727-lab.nii.gz rd728-lab.nii.gz rd729-lab.nii.gz rd730-lab.nii.gz rd731-lab.nii.gz rd732-lab.nii.gz rd734-lab.nii.gz rd735-lab.nii.gz rd736-lab.nii.gz rd737-lab.nii.gz rd738-lab.nii.gz rd739-lab.nii.gz rd740-lab.nii.gz rd741-lab.nii.gz rd743-lab.nii.gz rd744-lab.nii.gz rd745-lab.nii.gz rd747-lab.nii.gz rd748-lab.nii.gz rd749-lab.nii.gz rd750-lab.nii.gz rd752-lab.nii.gz rd753-lab.nii.gz rd754-lab.nii.gz rd755-lab.nii.gz frame.nii.gz

#/data/adamt/build/antsbin/bin/AverageImages 3 rhtemplate1.nii.gz 1 rd701-t1.nii.gz rd702-t1.nii.gz rd703-t1.nii.gz rd704-t1.nii.gz rd705-t1.nii.gz rd706-t1.nii.gz rd707-t1.nii.gz rd708-t1.nii.gz rd709-t1.nii.gz rd710-t1.nii.gz rd711-t1.nii.gz rd712-t1.nii.gz rd713-t1.nii.gz rd714-t1.nii.gz rd715-t1.nii.gz rd716-t1.nii.gz rd717-t1.nii.gz rd720-t1.nii.gz rd722-t1.nii.gz rd723-t1.nii.gz rd724-t1.nii.gz rd726-t1.nii.gz rd727-t1.nii.gz rd728-t1.nii.gz rd729-t1.nii.gz rd730-t1.nii.gz rd731-t1.nii.gz rd732-t1.nii.gz rd734-t1.nii.gz rd735-t1.nii.gz rd736-t1.nii.gz rd737-t1.nii.gz rd738-t1.nii.gz rd739-t1.nii.gz rd740-t1.nii.gz rd741-t1.nii.gz rd743-t1.nii.gz rd744-t1.nii.gz rd745-t1.nii.gz rd747-t1.nii.gz rd748-t1.nii.gz rd749-t1.nii.gz rd750-t1.nii.gz rd752-t1.nii.gz rd753-t1.nii.gz rd754-t1.nii.gz rd755-t1.nii.gz frame.nii.gz

#/data/adamt/build/antsbin/bin/AverageImages 3 rhtemplate2.nii.gz 1 rd701-t2s.nii.gz rd702-t2s.nii.gz rd703-t2s.nii.gz rd704-t2s.nii.gz rd705-t2s.nii.gz rd706-t2s.nii.gz rd707-t2s.nii.gz rd708-t2s.nii.gz rd709-t2s.nii.gz rd710-t2s.nii.gz rd711-t2s.nii.gz rd712-t2s.nii.gz rd713-t2s.nii.gz rd714-t2s.nii.gz rd715-t2s.nii.gz rd716-t2s.nii.gz rd717-t2s.nii.gz rd720-t2s.nii.gz rd722-t2s.nii.gz rd723-t2s.nii.gz rd724-t2s.nii.gz rd726-t2s.nii.gz rd727-t2s.nii.gz rd728-t2s.nii.gz rd729-t2s.nii.gz rd730-t2s.nii.gz rd731-t2s.nii.gz rd732-t2s.nii.gz rd734-t2s.nii.gz rd735-t2s.nii.gz rd736-t2s.nii.gz rd737-t2s.nii.gz rd738-t2s.nii.gz rd739-t2s.nii.gz rd740-t2s.nii.gz rd741-t2s.nii.gz rd743-t2s.nii.gz rd744-t2s.nii.gz rd745-t2s.nii.gz rd747-t2s.nii.gz rd748-t2s.nii.gz rd749-t2s.nii.gz rd750-t2s.nii.gz rd752-t2s.nii.gz rd753-t2s.nii.gz rd754-t2s.nii.gz rd755-t2s.nii.gz frame.nii.gz
