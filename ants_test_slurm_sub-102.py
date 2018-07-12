
# coding: utf-8

# In[17]:

# Import modules and set experiment-specific parameters
import copy
import os
import numpy as np
from os.path import join as opj
from nipype.pipeline.engine import Workflow, Node, MapNode, JoinNode
from nipype.interfaces.io import SelectFiles, DataSink
from nipype.interfaces.utility import IdentityInterface, Merge, Select
from nipype.interfaces.ants import Registration, ApplyTransforms, AverageImages, CreateJacobianDeterminantImage
from nipype import config, logging
from nipype.interfaces.freesurfer import MRIConvert

config.enable_debug_mode()
logging.update_logging(config)

#runs out of current directory 
filepath = os.path.dirname( os.path.realpath( '__file__'))
datadir = os.path.realpath(os.path.join(filepath, ''))
os.chdir(datadir)

#Baseline scans only
# subject_list = ['sub-102_ses-20120117', 'sub-103_ses-20120130', 'sub-104_ses-20120227', 'sub-105_ses-20120313', 
#                 'sub-106_ses-20120409', 'sub-107_ses-20120507', 'sub-109_ses-20120716', 'sub-108_ses-20120521'
#                 'sub-110_ses-20120730', 'sub-111_ses-20120910', 'sub-112_ses-20121119', 'sub-114_ses-20130225', 
#                 'sub-115_ses-20130325', 'sub-116_ses-20130408', 'sub-118_ses-20130506', 'sub-120_ses-20130729', 
#                 'sub-121_ses-20130826', 'sub-122_ses-20131104', 'sub-123_ses-20131202', 'sub-124_ses-20140127',
#                 'sub-125_ses-20140505', 'sub-126_ses-20140519', 'sub-127_ses-20141117', 'sub-128_ses-20150209', 
#                 'sub-130_ses-20150323', 'sub-131_ses-20150419', 'sub-133_ses-20150824', 'sub-134_ses-20150909', 
#                 'sub-135_ses-20160209', 'sub-136_ses-20160418', 'sub-138_ses-20160724', 'sub-139_ses-20160822', 
#                 'sub-301_ses-20110801', 'sub-302_ses-20110912', 'sub-304_ses-20111122', 'sub-306_ses-20140210', 
#                 'sub-308_ses-20140602', 'sub-309_ses-20140630', 'sub-310_ses-20140908', 'sub-311_ses-20140921', 
#                 'sub-312_ses-20141020', 'sub-313_ses-20141102', 'sub-314_ses-20150112', 'sub-315_ses-20150629',
#                 'sub-316_ses-20150630', 'sub-317_ses-20150906', 'sub-318_ses-20150921', 'sub-320_ses-20151228',
#                 'sub-321_ses-20160115', 'sub-322_ses-20160127', 'sub-323_ses-20160208', 'sub-324_ses-20160222', 
#                 'sub-327_ses-20160502']

#All scans
subject_list = ['sub-102_ses-20120117', 'sub-102_ses-20120120', 'sub-102_ses-20120131', 'sub-102_ses-20120214'
#                 'sub-103_ses-20120130', 'sub-103_ses-20120203', 'sub-104_ses-20120227', 'sub-104_ses-20120301', 
#                 'sub-104_ses-20120312', 'sub-104_ses-20120316', 'sub-104_ses-20120327', 'sub-105_ses-20120313', 
#                 'sub-105_ses-20120316', 'sub-105_ses-20120327', 'sub-105_ses-20120330', 'sub-105_ses-20120410', 
#                 'sub-106_ses-20120409', 'sub-106_ses-20120413', 'sub-106_ses-20120424', 'sub-106_ses-20120427', 
#                 'sub-106_ses-20120508', 'sub-107_ses-20120507', 'sub-107_ses-20120511', 'sub-107_ses-20120522', 
#                 'sub-107_ses-20120525', 'sub-107_ses-20120605', 'sub-108_ses-20120521', 'sub-108_ses-20120605', 
#                 'sub-108_ses-20120608', 'sub-108_ses-20120619', 'sub-109_ses-20120716', 'sub-109_ses-20120720', 
#                 'sub-109_ses-20120731', 'sub-109_ses-20120803', 'sub-109_ses-20120814', 'sub-110_ses-20120730', 
#                 'sub-110_ses-20120803', 'sub-110_ses-20120814', 'sub-110_ses-20120817', 'sub-110_ses-20120827',
#                 'sub-111_ses-20120910', 'sub-111_ses-20120914', 'sub-111_ses-20120925', 'sub-112_ses-20121119',
#                 'sub-112_ses-20121123', 'sub-112_ses-20121204', 'sub-112_ses-20121207', 'sub-112_ses-20121218', 
#                 'sub-114_ses-20130225', 'sub-114_ses-20130301', 'sub-114_ses-20130312', 'sub-114_ses-20130315', 
#                 'sub-114_ses-20130326', 'sub-115_ses-20130325', 'sub-115_ses-20130329', 'sub-115_ses-20130409', 
#                 'sub-115_ses-20130412', 'sub-115_ses-20130423', 'sub-116_ses-20130408', 'sub-116_ses-20130412', 
#                 'sub-116_ses-20130421', 'sub-116_ses-20130426', 'sub-116_ses-20130507', 'sub-118_ses-20130506',
#                 'sub-118_ses-20130510', 'sub-118_ses-20130521', 'sub-120_ses-20130729', 'sub-120_ses-20130802', 
#                 'sub-120_ses-20130816', 'sub-120_ses-20130827', 'sub-121_ses-20130826', 'sub-121_ses-20130830', 
#                 'sub-121_ses-20130910', 'sub-122_ses-20131104', 'sub-122_ses-20131108', 'sub-122_ses-20131119', 
#                 'sub-122_ses-20131122', 'sub-122_ses-20131201', 'sub-123_ses-20131202', 'sub-123_ses-20131206', 
#                 'sub-123_ses-20131216', 'sub-123_ses-20131220', 'sub-123_ses-20131229', 'sub-124_ses-20140127',
#                 'sub-124_ses-20140131', 'sub-124_ses-20140211', 'sub-124_ses-20140214', 'sub-124_ses-20140223',
#                 'sub-125_ses-20140505', 'sub-125_ses-20140509', 'sub-126_ses-20140519', 'sub-126_ses-20140523', 
#                 'sub-126_ses-20140603', 'sub-126_ses-20140606', 'sub-126_ses-20140615', 'sub-127_ses-20141117',
#                 'sub-127_ses-20141121', 'sub-127_ses-20141202', 'sub-127_ses-20141205', 'sub-127_ses-20141216',
#                 'sub-128_ses-20150209', 'sub-128_ses-20150213', 'sub-128_ses-20150224', 'sub-128_ses-20150227',
#                 'sub-128_ses-20150310', 'sub-130_ses-20150323', 'sub-130_ses-20150327', 'sub-130_ses-20150407', 
#                 'sub-130_ses-20150410', 'sub-130_ses-20150421', 'sub-131_ses-20150419', 'sub-131_ses-20150424',
#                 'sub-131_ses-20150505', 'sub-131_ses-20150508', 'sub-131_ses-20150519', 'sub-133_ses-20150824',
#                 'sub-133_ses-20150828', 'sub-133_ses-20150906', 'sub-133_ses-20150911', 'sub-133_ses-20150922', 
#                 'sub-134_ses-20150909', 'sub-134_ses-20150911', 'sub-134_ses-20150920', 'sub-134_ses-20150925', 
#                 'sub-134_ses-20151006', 'sub-135_ses-20160209', 'sub-135_ses-20160212', 'sub-135_ses-20160221',
#                 'sub-135_ses-20160226', 'sub-135_ses-20160308', 'sub-136_ses-20160418', 'sub-136_ses-20160421',
#                 'sub-136_ses-20160502', 'sub-136_ses-20160506', 'sub-138_ses-20160724', 'sub-138_ses-20160729', 
#                 'sub-138_ses-20160807', 'sub-139_ses-20160822', 'sub-139_ses-20160826', 'sub-139_ses-20160906',
#                 'sub-139_ses-20160909', 'sub-301_ses-20110801', 'sub-301_ses-20110805', 'sub-301_ses-20110815',
#                 'sub-301_ses-20110819', 'sub-301_ses-20110829', 'sub-302_ses-20110912', 'sub-302_ses-20110916', 
#                 'sub-304_ses-20111122', 'sub-304_ses-20111125', 'sub-304_ses-20111206', 'sub-304_ses-20111209',
#                 'sub-304_ses-20111220', 'sub-306_ses-20140210', 'sub-306_ses-20140214', 'sub-306_ses-20140225', 
#                 'sub-306_ses-20140228', 'sub-306_ses-20140309', 'sub-307_ses-20140421', 'sub-307_ses-20140425', 
#                 'sub-307_ses-20140506', 'sub-307_ses-20140509', 'sub-307_ses-20140519', 'sub-308_ses-20140602', 
#                 'sub-308_ses-20140606', 'sub-308_ses-20140617', 'sub-308_ses-20140629', 'sub-309_ses-20140630', 
#                 'sub-309_ses-20140704', 'sub-309_ses-20140715', 'sub-309_ses-20140718', 'sub-309_ses-20140729', 
#                 'sub-310_ses-20140908', 'sub-311_ses-20140921', 'sub-312_ses-20141020', 'sub-313_ses-20141102', 
#                 'sub-313_ses-20141107', 'sub-313_ses-20141116', 'sub-313_ses-20141121', 'sub-313_ses-20141130', 
#                 'sub-314_ses-20150112', 'sub-314_ses-20150116', 'sub-314_ses-20150127', 'sub-314_ses-20150130', 
#                 'sub-314_ses-20150210', 'sub-315_ses-20150629', 'sub-315_ses-20150703', 'sub-316_ses-20150630', 
#                 'sub-316_ses-20150703', 'sub-316_ses-20150717', 'sub-317_ses-20150906', 'sub-317_ses-20150910',
#                 'sub-318_ses-20150921', 'sub-318_ses-20150925', 'sub-318_ses-20151004', 'sub-318_ses-20151009', 
#                 'sub-318_ses-20151018', 'sub-320_ses-20151228', 'sub-320_ses-20160101', 'sub-320_ses-20160115',
#                 'sub-321_ses-20160115', 'sub-321_ses-20160129', 'sub-322_ses-20160127', 'sub-322_ses-20160202',
#                 'sub-322_ses-20160212', 'sub-323_ses-20160208', 'sub-324_ses-20160222', 'sub-324_ses-20160225',
#                 'sub-324_ses-20160311', 'sub-327_ses-20160502', 'sub-327_ses-20160506', 'sub-327_ses-20160519'
]

# Rigid Reg node 1

antsreg = Registration()
antsreg.inputs.float = True
antsreg.inputs.collapse_output_transforms=True
antsreg.inputs.output_transform_prefix = 'rigid_'
antsreg.inputs.fixed_image=[]
antsreg.inputs.moving_image=[]
antsreg.inputs.initial_moving_transform_com=1
antsreg.inputs.output_warped_image= True
antsreg.inputs.transforms=['Rigid']
antsreg.inputs.terminal_output='file'
antsreg.inputs.winsorize_lower_quantile=0.005
antsreg.inputs.winsorize_upper_quantile=0.995
antsreg.inputs.convergence_threshold=[1e-06]
antsreg.inputs.convergence_window_size=[10]
antsreg.inputs.metric=[['MeanSquares','MI','MI']]
antsreg.inputs.metric_weight=[[0.75,0.25,0.0]]
antsreg.inputs.number_of_iterations=[[1000, 500, 250, 0]]
antsreg.inputs.smoothing_sigmas=[[4, 3, 2, 1]]
antsreg.inputs.sigma_units=['vox']
antsreg.inputs.radius_or_number_of_bins=[[0,32,32]]
antsreg.inputs.sampling_strategy=[['None',
                               'Regular',
                               'Regular']]
antsreg.inputs.sampling_percentage=[[0,0.25,0.25]]
antsreg.inputs.shrink_factors=[[12,8,4,2]]
antsreg.inputs.transform_parameters=[[(0.1)]]
antsreg.inputs.use_histogram_matching=True

antsreg_rigid = Node(antsreg,name='antsreg_rigid')
#antsreg.cmdline

# Apply Rigid Reg node 1

apply_rigid_reg = ApplyTransforms()

apply_rigid = MapNode(apply_rigid_reg, 
                      name = 'apply_rigid', 
                      iterfield=['input_image','reference_image','transforms'], 
                      nested = True
                     )
apply_rigid.inputs.input_image = []
apply_rigid.inputs.reference_image = []
apply_rigid.inputs.transforms = []
apply_rigid.inputs.terminal_output = 'file'
#apply_rigid_reg.cmdline

# Select outputs by image type

# Select labels

sl = Select()
sl = Node(sl, name = 'select_lists')
sl.inputs.inlist= []
sl.inputs.index=[]
sl.iterables = ('index', [0,1,2])

# Merge selected files into list

ml = Merge(1)
ml = JoinNode(ml, 
              name = 'merge_lists',
             joinsource = 'info_source',
             joinfield = 'in1')
ml.inputs.in1 = []
ml.inputs.axis = 'hstack'

# Average rigid-transformed images to construct new template

avg_rigid = AverageImages()
avg_rigid = Node(avg_rigid, name = 'average_rigid')
avg_rigid.inputs.dimension = 3
avg_rigid.inputs.images = []
avg_rigid.inputs.normalize = True
avg_rigid.inputs.terminal_output = 'file'
#avg_rigid.cmdline

#convert average.nii to nii.gz

mc = MRIConvert()
mc.inputs.out_type = 'niigz'
mc = Node(mc, name = 'mri_convert')

# Rigid Reg node 2

antsreg2 = Registration()
antsreg2.inputs.float = True
antsreg2.inputs.collapse_output_transforms=True
antsreg2.inputs.output_transform_prefix = 'rigid_'
antsreg2.inputs.fixed_image=[]
antsreg2.inputs.moving_image=[]
antsreg2.inputs.initial_moving_transform_com=1
antsreg2.inputs.output_warped_image= True
antsreg2.inputs.transforms=['Rigid']
antsreg2.inputs.terminal_output='file'
antsreg2.inputs.winsorize_lower_quantile=0.005
antsreg2.inputs.winsorize_upper_quantile=0.995
antsreg2.inputs.convergence_threshold=[1e-06]
antsreg2.inputs.convergence_window_size=[10]
antsreg2.inputs.metric=[['MeanSquares','MI','MI']]
antsreg2.inputs.metric_weight=[[0.75,0.25,0.0]]
antsreg2.inputs.number_of_iterations=[[1000, 500, 250, 0]]
antsreg2.inputs.smoothing_sigmas=[[4, 3, 2, 1]]
antsreg2.inputs.sigma_units=['vox']
antsreg2.inputs.radius_or_number_of_bins=[[0,32,32]]
antsreg2.inputs.sampling_strategy=[['None',
                               'Regular',
                               'Regular']]
antsreg2.inputs.sampling_percentage=[[0,0.25,0.25]]
antsreg2.inputs.shrink_factors=[[12,8,4,2]]
antsreg2.inputs.transform_parameters=[[(0.1)]]
antsreg2.inputs.use_histogram_matching=True

antsreg_rigid2 = Node(antsreg2, name='antsreg_rigid_2')

# Apply Rigid Reg node 2

apply_rigid_reg2 = ApplyTransforms()
apply_rigid2 = MapNode(apply_rigid_reg2, 
                      name = 'apply_rigid_2', 
                      iterfield=['input_image','reference_image','transforms'], 
                      nested = True
                     )
apply_rigid2.inputs.input_image = []
apply_rigid2.inputs.reference_image = []
apply_rigid2.inputs.transforms = []
apply_rigid2.inputs.terminal_output = 'file'
#apply_rigid_reg.cmdline

# Select outputs by image type

# Select labels

sl2 = Select()
sl2 = Node(sl2, name = 'select_lists_2')
sl2.inputs.inlist= []
sl2.inputs.index=[]
sl2.iterables = ('index', [0,1,2])

# Merge selected files into list

ml3 = Merge(1)
ml3 = JoinNode(ml3, 
               name = 'merge_lists_3',
               joinsource = 'info_source_2',
               joinfield = 'in1')
ml3.inputs.in1 = []
ml3.inputs.axis = 'hstack'

# Average rigid-transformed images to construct new template

avg_rigid2 = AverageImages()
avg_rigid2 = Node(avg_rigid2, name = 'average_rigid_2')
avg_rigid2.inputs.dimension = 3
avg_rigid2.inputs.images = []
avg_rigid2.inputs.normalize = True
avg_rigid2.inputs.terminal_output = 'file'

#convert average.nii to nii.gz

mc2 = MRIConvert()
mc2.inputs.out_type = 'niigz'
mc2 = Node(mc2, name = 'mri_convert_2')

# Rigid Reg node 3

antsreg3 = Registration()
antsreg3.inputs.float = True
antsreg3.inputs.collapse_output_transforms=True
antsreg3.inputs.output_transform_prefix = 'rigid_'
antsreg3.inputs.fixed_image=[]
antsreg3.inputs.moving_image=[]
antsreg3.inputs.initial_moving_transform_com=1
antsreg3.inputs.output_warped_image= True
antsreg3.inputs.transforms=['Rigid']
antsreg3.inputs.terminal_output='file'
antsreg3.inputs.winsorize_lower_quantile=0.005
antsreg3.inputs.winsorize_upper_quantile=0.995
antsreg3.inputs.convergence_threshold=[1e-06]
antsreg3.inputs.convergence_window_size=[10]
antsreg3.inputs.metric=[['MeanSquares','MI','MI']]
antsreg3.inputs.metric_weight=[[0.75,0.25,0.0]]
antsreg3.inputs.number_of_iterations=[[1000, 500, 250, 0]]
antsreg3.inputs.smoothing_sigmas=[[4, 3, 2, 1]]
antsreg3.inputs.sigma_units=['vox']
antsreg3.inputs.radius_or_number_of_bins=[[0,32,32]]
antsreg3.inputs.sampling_strategy=[['None',
                               'Regular',
                               'Regular']]
antsreg3.inputs.sampling_percentage=[[0,0.25,0.25]]
antsreg3.inputs.shrink_factors=[[12,8,4,2]]
antsreg3.inputs.transform_parameters=[[(0.1)]]
antsreg3.inputs.use_histogram_matching=True

antsreg_rigid3 = Node(antsreg3, name='antsreg_rigid_3')

# Apply Rigid Reg node 3

apply_rigid_reg3 = ApplyTransforms()
apply_rigid3 = MapNode(apply_rigid_reg3, 
                      name = 'apply_rigid_3', 
                      iterfield=['input_image','reference_image','transforms'], 
                      nested = True
                     )
apply_rigid3.inputs.input_image = []
apply_rigid3.inputs.reference_image = []
apply_rigid3.inputs.transforms = []
apply_rigid3.inputs.terminal_output = 'file'
#apply_rigid_reg.cmdline

# Select outputs by image type

# Select labels

sl3 = Select()
sl3 = Node(sl3, name = 'select_lists_3')
sl3.inputs.inlist= []
sl3.inputs.index=[]
sl3.iterables = ('index', [0,1,2])

# Merge selected files into list

ml4 = Merge(1)
ml4 = JoinNode(ml4, 
               name = 'merge_lists_4',
               joinsource = 'info_source_3',
               joinfield = 'in1')
ml4.inputs.in1 = []
ml4.inputs.axis = 'hstack'

# Average rigid-transformed images to construct new template

avg_rigid3 = AverageImages()
avg_rigid3 = Node(avg_rigid3, name = 'average_rigid_3')
avg_rigid3.inputs.dimension = 3
avg_rigid3.inputs.images = []
avg_rigid3.inputs.normalize = True
avg_rigid3.inputs.terminal_output = 'file'

#convert average.nii to nii.gz

mc3 = MRIConvert()
mc3.inputs.out_type = 'niigz'
mc3 = Node(mc3, name = 'mri_convert_3')

# Affine Reg Node 1
antsreg4 = Registration()
antsreg4.inputs.float = True
antsreg4.inputs.collapse_output_transforms=True
antsreg4.inputs.output_transform_prefix = 'affine_'
antsreg4.inputs.fixed_image=[]
antsreg4.inputs.moving_image=[]
antsreg4.inputs.initial_moving_transform_com=1
antsreg4.inputs.output_warped_image= True
antsreg4.inputs.transforms=['Rigid','Affine']
antsreg4.inputs.terminal_output='file'
antsreg4.inputs.winsorize_lower_quantile=0.005
antsreg4.inputs.winsorize_upper_quantile=0.995
antsreg4.inputs.convergence_threshold=[1e-06]
antsreg4.inputs.convergence_window_size=[10]
antsreg4.inputs.metric=[['MeanSquares','MI','MI']]*2
antsreg4.inputs.metric_weight=[[0.75,0.25,0.0]]*2
antsreg4.inputs.number_of_iterations=[[1000, 500, 250, 0]]*2
antsreg4.inputs.smoothing_sigmas=[[4, 3, 2, 1]]*2
antsreg4.inputs.sigma_units=['vox']*2
antsreg4.inputs.radius_or_number_of_bins=[[0,32,32]]*2
antsreg4.inputs.sampling_strategy=[['None',
                               'Regular',
                               'Regular']]*2
antsreg4.inputs.sampling_percentage=[[0,0.25,0.25]]*2
antsreg4.inputs.shrink_factors=[[12,8,4,2]]*2
antsreg4.inputs.transform_parameters=[[(0.1)]]*2
antsreg4.inputs.use_histogram_matching=True

antsreg_affine1 = Node(antsreg4, name='antsreg_affine_1')


# Apply Affine Reg node 1

apply_affine_reg1 = ApplyTransforms()
apply_affine1 = MapNode(apply_affine_reg1, 
                      name = 'apply_affine_1', 
                      iterfield=['input_image','reference_image','transforms'], 
                      nested = True
                     )
apply_affine1.inputs.input_image = []
apply_affine1.inputs.reference_image = []
apply_affine1.inputs.transforms = []
apply_affine1.inputs.terminal_output = 'file'
#apply_rigid_reg.cmdline

# Select outputs by image type

# Select labels

sl4 = Select()
sl4 = Node(sl4, name = 'select_lists_4')
sl4.inputs.inlist= []
sl4.inputs.index=[]
sl4.iterables = ('index', [0,1,2])

# Merge selected files into list

ml5 = Merge(1)
ml5 = JoinNode(ml5, 
               name = 'merge_lists_5',
               joinsource = 'info_source_4',
               joinfield = 'in1')
ml5.inputs.in1 = []
ml5.inputs.axis = 'hstack'

# Average rigid-transformed images to construct new template

avg_affine1 = AverageImages()
avg_affine1 = Node(avg_affine1, name = 'average_affine_1')
avg_affine1.inputs.dimension = 3
avg_affine1.inputs.images = []
avg_affine1.inputs.normalize = True
avg_affine1.inputs.terminal_output = 'file'

#convert average.nii to nii.gz

mc4 = MRIConvert()
mc4.inputs.out_type = 'niigz'
mc4 = Node(mc4, name = 'mri_convert_4')

# Affine Reg Node 2
antsreg5 = Registration()
antsreg5.inputs.float = True
antsreg5.inputs.collapse_output_transforms=True
antsreg5.inputs.output_transform_prefix = 'affine_'
antsreg5.inputs.fixed_image=[]
antsreg5.inputs.moving_image=[]
antsreg5.inputs.initial_moving_transform_com=1
antsreg5.inputs.output_warped_image= True
antsreg5.inputs.transforms=['Rigid','Affine']
antsreg5.inputs.terminal_output='file'
antsreg5.inputs.winsorize_lower_quantile=0.005
antsreg5.inputs.winsorize_upper_quantile=0.995
antsreg5.inputs.convergence_threshold=[1e-06]
antsreg5.inputs.convergence_window_size=[10]
antsreg5.inputs.metric=[['MeanSquares','MI','MI']]*2
antsreg5.inputs.metric_weight=[[0.75,0.25,0.0]]*2
antsreg5.inputs.number_of_iterations=[[1000, 500, 250, 0]]*2
antsreg5.inputs.smoothing_sigmas=[[4, 3, 2, 1]]*2
antsreg5.inputs.sigma_units=['vox']*2
antsreg5.inputs.radius_or_number_of_bins=[[0,32,32]]*2
antsreg5.inputs.sampling_strategy=[['None',
                               'Regular',
                               'Regular']]*2
antsreg5.inputs.sampling_percentage=[[0,0.25,0.25]]*2
antsreg5.inputs.shrink_factors=[[12,8,4,2]]*2
antsreg5.inputs.transform_parameters=[[(0.1)]]*2
antsreg5.inputs.use_histogram_matching=True

antsreg_affine2 = Node(antsreg5, name='antsreg_affine_2')

# Apply Affine Reg node 2

apply_affine_reg2 = ApplyTransforms()
apply_affine2 = MapNode(apply_affine_reg2, 
                      name = 'apply_affine_2', 
                      iterfield=['input_image','reference_image','transforms'], 
                      nested = True
                     )
apply_affine2.inputs.input_image = []
apply_affine2.inputs.reference_image = []
apply_affine2.inputs.transforms = []
apply_affine2.inputs.terminal_output = 'file'
#apply_rigid_reg.cmdline

# Select outputs by image type

# Select labels

sl5 = Select()
sl5 = Node(sl5, name = 'select_lists_5')
sl5.inputs.inlist= []
sl5.inputs.index=[]
sl5.iterables = ('index', [0,1,2])

# Merge selected files into list

ml6 = Merge(1)
ml6 = JoinNode(ml6, 
               name = 'merge_lists_6',
               joinsource = 'info_source_5',
               joinfield = 'in1')
ml6.inputs.in1 = []
ml6.inputs.axis = 'hstack'

# Average rigid-transformed images to construct new template

avg_affine2 = AverageImages()
avg_affine2 = Node(avg_affine2, name = 'average_affine_2')
avg_affine2.inputs.dimension = 3
avg_affine2.inputs.images = []
avg_affine2.inputs.normalize = True
avg_affine2.inputs.terminal_output = 'file'

#convert average.nii to nii.gz

mc5 = MRIConvert()
mc5.inputs.out_type = 'niigz'
mc5 = Node(mc5, name = 'mri_convert_5')

# BSpline Reg Node 1
antsreg6 = Registration()
antsreg6.inputs.float = True
antsreg6.inputs.output_transform_prefix = 'BSplineSyN_'
antsreg6.inputs.write_composite_transform = True
antsreg6.inputs.fixed_image=[]
antsreg6.inputs.moving_image=[]
antsreg6.inputs.initial_moving_transform_com=1
antsreg6.inputs.transforms=['Rigid','Affine','BSplineSyN']
antsreg6.inputs.terminal_output='file'
antsreg6.inputs.winsorize_lower_quantile=0.005
antsreg6.inputs.winsorize_upper_quantile=0.995
antsreg6.inputs.convergence_threshold=[1e-06]
antsreg6.inputs.convergence_window_size=[10]
antsreg6.inputs.metric=[['MeanSquares','MI','MI'],
                        ['MeanSquares','MI','MI'],
                        ['MeanSquares','CC','CC']]
antsreg6.inputs.metric_weight=[[0.75,0.25,0.0],
                               [0.75,0.25,0.0],
                               [0.10,0.90,0.0]]
antsreg6.inputs.number_of_iterations=[[1000,500,250,0],
                                      [1000,500,250,0],
                                      [100, 100, 70, 50, 0]]
antsreg6.inputs.smoothing_sigmas=[[4,3,2,1],
                                  [4,3,2,1],
                                  [5, 3, 2, 1, 0]]
antsreg6.inputs.sigma_units=['vox']*3
antsreg6.inputs.radius_or_number_of_bins=[[0,32,32],
                                          [0,32,32],
                                          [0,2,2]]
antsreg6.inputs.sampling_strategy=[['None', 'Regular', 'Regular'],
                                   ['None', 'Regular', 'Regular'],
                                   ['None', 'None', 'None']]
antsreg6.inputs.sampling_percentage=[[0,0.25,0.25],
                                    [0,0.25,0.25],
                                    [1,1,1]]
antsreg6.inputs.shrink_factors=[[12,8,4,2],
                                [12,8,4,2],
                                [10,6,4,2,1]]
antsreg6.inputs.transform_parameters= [[(0.1)], [(0.1)],[0.1, 26, 0, 3]]
antsreg6.inputs.use_histogram_matching= False

antsreg_BSpline1 = Node(antsreg6, name='antsreg_BSplineSyn_1')


# Apply BSplineSyN Reg node 1

apply_BSpline_reg1 = ApplyTransforms()
apply_BSpline1 = MapNode(apply_BSpline_reg1, 
                      name = 'apply_BSpline_1', 
                      iterfield=['input_image','reference_image','transforms'], 
                      nested = True
                     )
apply_BSpline1.inputs.input_image = []
apply_BSpline1.inputs.reference_image = []
apply_BSpline1.inputs.transforms = []
apply_BSpline1.inputs.terminal_output = 'file'
#apply_rigid_reg.cmdline

# Select outputs by image type

# Select labels

sl6 = Select()
sl6 = Node(sl6, name = 'select_lists_6')
sl6.inputs.inlist= []
sl6.inputs.index=[]
sl6.iterables = ('index', [0,1,2])

# Merge selected files into list

ml7 = Merge(1)
ml7 = JoinNode(ml7, 
               name = 'merge_lists_7',
               joinsource = 'info_source_6',
               joinfield = 'in1')
ml7.inputs.in1 = []
ml7.inputs.axis = 'hstack'

# Average rigid-transformed images to construct new template

avg_BSpline1 = AverageImages()
avg_BSpline1 = Node(avg_BSpline1, name = 'average_BSpline_1')
avg_BSpline1.inputs.dimension = 3
avg_BSpline1.inputs.images = []
avg_BSpline1.inputs.normalize = True
avg_BSpline1.inputs.terminal_output = 'file'

#convert average.nii to nii.gz

mc6 = MRIConvert()
mc6.inputs.out_type = 'niigz'
mc6 = Node(mc6, name = 'mri_convert_6')

# BSpline Reg Node 2
antsreg7 = Registration()
antsreg7.inputs.float = True
antsreg7.inputs.output_transform_prefix = 'BSplineSyN_'
antsreg7.inputs.write_composite_transform = True
antsreg7.inputs.fixed_image=[]
antsreg7.inputs.moving_image=[]
antsreg7.inputs.initial_moving_transform_com=1
antsreg7.inputs.transforms=['Rigid','Affine','BSplineSyN']
antsreg7.inputs.terminal_output='file'
antsreg7.inputs.winsorize_lower_quantile=0.005
antsreg7.inputs.winsorize_upper_quantile=0.995
antsreg7.inputs.convergence_threshold=[1e-06]
antsreg7.inputs.convergence_window_size=[10]
antsreg7.inputs.metric=[['MeanSquares','MI','MI'],
                        ['MeanSquares','MI','MI'],
                        ['MeanSquares','CC','CC']]
antsreg7.inputs.metric_weight=[[0.75,0.25,0.0],
                               [0.75,0.25,0.0],
                               [0.10,0.90,0.0]]
antsreg7.inputs.number_of_iterations=[[1000,500,250,0],
                                      [1000,500,250,0],
                                      [100, 100, 70, 50, 0]]
antsreg7.inputs.smoothing_sigmas=[[4,3,2,1],
                                  [4,3,2,1],
                                  [5, 3, 2, 1, 0]]
antsreg7.inputs.sigma_units=['vox']*3
antsreg7.inputs.radius_or_number_of_bins=[[0,32,32],
                                          [0,32,32],
                                          [0,2,2]]
antsreg7.inputs.sampling_strategy=[['None', 'Regular', 'Regular'],
                                   ['None', 'Regular', 'Regular'],
                                   ['None', 'None', 'None']]
antsreg7.inputs.sampling_percentage=[[0,0.25,0.25],
                                    [0,0.25,0.25],
                                    [1,1,1]]
antsreg7.inputs.shrink_factors=[[12,8,4,2],
                                [12,8,4,2],
                                [10,6,4,2,1]]
antsreg7.inputs.transform_parameters= [[(0.1)], [(0.1)],[0.1, 26, 0, 3]]
antsreg7.inputs.use_histogram_matching= False

antsreg_BSpline2 = Node(antsreg7, name='antsreg_BSplineSyn_2')

# Apply BSplineSyN Reg node 1

apply_BSpline_reg2 = ApplyTransforms()
apply_BSpline2 = MapNode(apply_BSpline_reg2, 
                      name = 'apply_BSpline_2', 
                      iterfield=['input_image','reference_image','transforms'], 
                      nested = True
                     )
apply_BSpline2.inputs.input_image = []
apply_BSpline2.inputs.reference_image = []
apply_BSpline2.inputs.transforms = []
apply_BSpline2.inputs.terminal_output = 'file'
#apply_rigid_reg.cmdline

# Select outputs by image type

# Select labels

sl7 = Select()
sl7 = Node(sl7, name = 'select_lists_7')
sl7.inputs.inlist= []
sl7.inputs.index=[]
sl7.iterables = ('index', [0,1,2])

# Merge selected files into list

ml8 = Merge(1)
ml8 = JoinNode(ml8, 
               name = 'merge_lists_8',
               joinsource = 'info_source_7',
               joinfield = 'in1')
ml8.inputs.in1 = []
ml8.inputs.axis = 'hstack'

# Average rigid-transformed images to construct new template

avg_BSpline2 = AverageImages()
avg_BSpline2 = Node(avg_BSpline2, name = 'average_BSpline_2')
avg_BSpline2.inputs.dimension = 3
avg_BSpline2.inputs.images = []
avg_BSpline2.inputs.normalize = True
avg_BSpline2.inputs.terminal_output = 'file'

#convert average.nii to nii.gz

mc7 = MRIConvert()
mc7.inputs.out_type = 'niigz'
mc7 = Node(mc7, name = 'mri_convert_7')

# BSpline Reg Node 3
antsreg8 = Registration()
antsreg8.inputs.float = True
antsreg8.inputs.output_transform_prefix = 'BSplineSyN_'
antsreg8.inputs.write_composite_transform = True
antsreg8.inputs.fixed_image=[]
antsreg8.inputs.moving_image=[]
antsreg8.inputs.initial_moving_transform_com=1
antsreg8.inputs.transforms=['Rigid','Affine','BSplineSyN']
antsreg8.inputs.terminal_output='file'
antsreg8.inputs.winsorize_lower_quantile=0.005
antsreg8.inputs.winsorize_upper_quantile=0.995
antsreg8.inputs.convergence_threshold=[1e-06]
antsreg8.inputs.convergence_window_size=[10]
antsreg8.inputs.metric=[['MeanSquares','MI','MI'],
                        ['MeanSquares','MI','MI'],
                        ['MeanSquares','CC','CC']]
antsreg8.inputs.metric_weight=[[0.75,0.25,0.0],
                               [0.75,0.25,0.0],
                               [0.10,0.90,0.0]]
antsreg8.inputs.number_of_iterations=[[1000,500,250,0],
                                      [1000,500,250,0],
                                      [100, 100, 70, 50, 0]]
antsreg8.inputs.smoothing_sigmas=[[4,3,2,1],
                                  [4,3,2,1],
                                  [5, 3, 2, 1, 0]]
antsreg8.inputs.sigma_units=['vox']*3
antsreg8.inputs.radius_or_number_of_bins=[[0,32,32],
                                          [0,32,32],
                                          [0,2,2]]
antsreg8.inputs.sampling_strategy=[['None', 'Regular', 'Regular'],
                                   ['None', 'Regular', 'Regular'],
                                   ['None', 'None', 'None']]
antsreg8.inputs.sampling_percentage=[[0,0.25,0.25],
                                    [0,0.25,0.25],
                                    [1,1,1]]
antsreg8.inputs.shrink_factors=[[12,8,4,2],
                                [12,8,4,2],
                                [10,6,4,2,1]]
antsreg8.inputs.transform_parameters= [[(0.1)], [(0.1)],[0.1, 26, 0, 3]]
antsreg8.inputs.use_histogram_matching= False

antsreg_BSpline3 = Node(antsreg8, name='antsreg_BSplineSyn_3')

# Apply BSplineSyN Reg node 1

apply_BSpline_reg3 = ApplyTransforms()
apply_BSpline3 = MapNode(apply_BSpline_reg3, 
                      name = 'apply_BSpline_3', 
                      iterfield=['input_image','reference_image','transforms'], 
                      nested = True
                     )
apply_BSpline3.inputs.input_image = []
apply_BSpline3.inputs.reference_image = []
apply_BSpline3.inputs.transforms = []
apply_BSpline3.inputs.terminal_output = 'file'
#apply_rigid_reg.cmdline

# Select outputs by image type

# Select labels

sl8 = Select()
sl8 = Node(sl8, name = 'select_lists_8')
sl8.inputs.inlist= []
sl8.inputs.index=[]
sl8.iterables = ('index', [0,1,2])

# Merge selected files into list

ml9 = Merge(1)
ml9 = JoinNode(ml9, 
               name = 'merge_lists_9',
               joinsource = 'info_source_8',
               joinfield = 'in1')
ml9.inputs.in1 = []
ml9.inputs.axis = 'hstack'

# Average rigid-transformed images to construct new template

avg_BSpline3 = AverageImages()
avg_BSpline3 = Node(avg_BSpline3, name = 'average_BSpline_3')
avg_BSpline3.inputs.dimension = 3
avg_BSpline3.inputs.images = []
avg_BSpline3.inputs.normalize = True
avg_BSpline3.inputs.terminal_output = 'file'

#convert average.nii to nii.gz

mc8 = MRIConvert()
mc8.inputs.out_type = 'niigz'
mc8_test = Node(mc8, name = 'mri_convert_8')

# BSpline Reg Node 4
antsreg9 = Registration()
antsreg9.inputs.float = True
antsreg9.inputs.output_transform_prefix = 'BSplineSyN_'
antsreg9.inputs.write_composite_transform = True
antsreg9.inputs.fixed_image=[]
antsreg9.inputs.moving_image=[]
antsreg9.inputs.initial_moving_transform_com=1
antsreg9.inputs.transforms=['Rigid','Affine','BSplineSyN']
antsreg9.inputs.terminal_output='file'
antsreg9.inputs.winsorize_lower_quantile=0.005
antsreg9.inputs.winsorize_upper_quantile=0.995
antsreg9.inputs.convergence_threshold=[1e-06]
antsreg9.inputs.convergence_window_size=[10]
antsreg9.inputs.metric=[['MeanSquares','MI','MI'],
                        ['MeanSquares','MI','MI'],
                        ['MeanSquares','CC','CC']]
antsreg9.inputs.metric_weight=[[0.75,0.25,0.0],
                               [0.75,0.25,0.0],
                               [0.10,0.90,0.0]]
antsreg9.inputs.number_of_iterations=[[1000,500,250,0],
                                      [1000,500,250,0],
                                      [100, 100, 70, 50, 0]]
antsreg9.inputs.smoothing_sigmas=[[4,3,2,1],
                                  [4,3,2,1],
                                  [5, 3, 2, 1, 0]]
antsreg9.inputs.sigma_units=['vox']*3
antsreg9.inputs.radius_or_number_of_bins=[[0,32,32],
                                          [0,32,32],
                                          [0,2,2]]
antsreg9.inputs.sampling_strategy=[['None', 'Regular', 'Regular'],
                                   ['None', 'Regular', 'Regular'],
                                   ['None', 'None', 'None']]
antsreg9.inputs.sampling_percentage=[[0,0.25,0.25],
                                    [0,0.25,0.25],
                                    [1,1,1]]
antsreg9.inputs.shrink_factors=[[12,8,4,2],
                                [12,8,4,2],
                                [10,6,4,2,1]]
antsreg9.inputs.transform_parameters= [[(0.1)], [(0.1)],[0.1, 26, 0, 3]]
antsreg9.inputs.use_histogram_matching= False

antsreg_BSpline4 = Node(antsreg9, name='antsreg_BSplineSyn_4')

# BSpline Reg Node 4a
antsreg9a = Registration()
antsreg9a.inputs.float = True
antsreg9a.inputs.output_transform_prefix = 'BSplineSyN_'
antsreg9a.inputs.write_composite_transform = True
antsreg9a.inputs.fixed_image=[]
antsreg9a.inputs.moving_image=[]
antsreg9a.inputs.initial_moving_transform_com=1
antsreg9a.inputs.transforms=['Rigid','Affine','BSplineSyN']
antsreg9a.inputs.terminal_output='file'
antsreg9a.inputs.winsorize_lower_quantile=0.005
antsreg9a.inputs.winsorize_upper_quantile=0.995
antsreg9a.inputs.convergence_threshold=[1e-06]
antsreg9a.inputs.convergence_window_size=[10]
antsreg9a.inputs.metric=[['MeanSquares','MI','MI'],
                        ['MeanSquares','MI','MI'],
                        ['MeanSquares','CC','CC']]
antsreg9a.inputs.metric_weight=[[0.75,0.25,0.0],
                               [0.75,0.25,0.0],
                               [0.10,0.90,0.0]]
antsreg9a.inputs.number_of_iterations=[[1000,500,250,0],
                                      [1000,500,250,0],
                                      [100, 100, 70, 50, 0]]
antsreg9a.inputs.smoothing_sigmas=[[4,3,2,1],
                                  [4,3,2,1],
                                  [5, 3, 2, 1, 0]]
antsreg9a.inputs.sigma_units=['vox']*3
antsreg9a.inputs.radius_or_number_of_bins=[[0,32,32],
                                          [0,32,32],
                                          [0,2,2]]
antsreg9a.inputs.sampling_strategy=[['None', 'Regular', 'Regular'],
                                   ['None', 'Regular', 'Regular'],
                                   ['None', 'None', 'None']]
antsreg9a.inputs.sampling_percentage=[[0,0.25,0.25],
                                    [0,0.25,0.25],
                                    [1,1,1]]
antsreg9a.inputs.shrink_factors=[[12,8,4,2],
                                [12,8,4,2],
                                [10,6,4,2,1]]
antsreg9a.inputs.transform_parameters= [[(0.1)], [(0.1)],[0.1, 26, 0, 3]]
antsreg9a.inputs.use_histogram_matching= False

antsreg_BSpline4a = Node(antsreg9a, name='antsreg_BSplineSyn_4a')

# Apply BSplineSyN Reg node 1

apply_BSpline_reg4 = ApplyTransforms()
apply_BSpline4 = MapNode(apply_BSpline_reg4, 
                      name = 'apply_BSpline_4', 
                      iterfield=['input_image','reference_image','transforms'], 
                      nested = True
                     )
apply_BSpline4.inputs.input_image = []
apply_BSpline4.inputs.reference_image = []
apply_BSpline4.inputs.transforms = []
apply_BSpline4.inputs.terminal_output = 'file'
#apply_rigid_reg.cmdline

# Select outputs by image type

# Select labels

sl9 = Select()
sl9 = Node(sl9, name = 'select_lists_9')
sl9.inputs.inlist= []
sl9.inputs.index=[]
sl9.iterables = ('index', [0,1,2])

# Merge selected files into list

ml10 = Merge(1)
ml10 = JoinNode(ml10, 
               name = 'merge_lists_10',
               joinsource = 'info_source_9',
               joinfield = 'in1')
ml10.inputs.in1 = []
ml10.inputs.axis = 'hstack'

# Average rigid-transformed images to construct new template

avg_BSpline4 = AverageImages()
avg_BSpline4 = Node(avg_BSpline4, name = 'average_BSpline_4')
avg_BSpline4.inputs.dimension = 3
avg_BSpline4.inputs.images = []
avg_BSpline4.inputs.normalize = True
avg_BSpline4.inputs.terminal_output = 'file'

#convert average.nii to nii.gz

mc9 = MRIConvert()
mc9.inputs.out_type = 'niigz'
mc9 = Node(mc9, name = 'mri_convert_9')

# Apply transforms and output warp file instead of transformed image

apply_BSpline_reg4a = ApplyTransforms()
apply_BSpline4a = MapNode(apply_BSpline_reg4a, 
                      name = 'apply_BSpline_4a', 
                      iterfield=['input_image','reference_image','transforms'], 
                      nested = True
                     )
apply_BSpline4a.inputs.input_image = []
apply_BSpline4a.inputs.reference_image = []
apply_BSpline4a.inputs.transforms = []
apply_BSpline4a.inputs.dimension = 3
apply_BSpline4a.inputs.output_image='outputDisplacementField.nii.gz'
apply_BSpline4a.inputs.print_out_composite_warp_file=True
apply_BSpline4a.inputs.terminal_output = 'file'

# Jacobian

jacobian = CreateJacobianDeterminantImage()
jacobian.inputs.imageDimension = 3
jacobian.inputs.outputImage = 'jacobian.nii.gz'
jacobian.inputs.doLogJacobian= 1
jacobian = Node(jacobian, name = 'jacobian')

#WORKFLOW 10 TEST

#Test warp on non-binarized hippo labels
apply_BSpline_reg5 = ApplyTransforms()
apply_BSpline5 = MapNode(apply_BSpline_reg5, 
                      name = 'apply_BSpline_5', 
                      iterfield=['input_image','reference_image','transforms'], 
                      nested = True
                     )
apply_BSpline5.inputs.input_image = []
apply_BSpline5.inputs.reference_image = ['/gpfs/gsfs6/users/Hippo_hr/cpb_2016-Dec/shape/normflow9/_index_0/mri_convert_9/average_out.nii.gz']
apply_BSpline5.inputs.transforms = []
apply_BSpline5.inputs.interpolation = 'MultiLabel'
apply_BSpline5.inputs.terminal_output = 'file'

# Select outputs by image type

# Select labels

sl10 = Select()
sl10 = Node(sl10, name = 'select_lists_10')
sl10.inputs.inlist= []
sl10.inputs.index=[]
sl10.iterables = ('index', [0])

# Merge selected files into list

ml11 = Merge(1)
ml11 = JoinNode(ml11, 
               name = 'merge_lists_11',
               joinsource = 'info_source_10',
               joinfield = 'in1')
ml11.inputs.in1 = []
ml11.inputs.axis = 'hstack'

# Average rigid-transformed images to construct new template

avg_BSpline5 = AverageImages()
avg_BSpline5 = Node(avg_BSpline5, name = 'average_BSpline_5')
avg_BSpline5.inputs.dimension = 3
avg_BSpline5.inputs.images = []
avg_BSpline5.inputs.normalize = True
avg_BSpline5.inputs.terminal_output = 'file'

                #convert average.nii to nii.gz

mc10 = MRIConvert()
mc10.inputs.out_type = 'niigz'
mc10 = Node(mc10, name = 'mri_convert_10')

# Establish input/output stream

# create subject ID iterable
infosource = Node(IdentityInterface(fields=['subject_id']), name = "info_source")
infosource.iterables = [('subject_id', subject_list)]

infosource2 = Node(IdentityInterface(fields=['subject_id']), name = "info_source_2")
infosource2.iterables = [('subject_id', subject_list)]

infosource3 = Node(IdentityInterface(fields=['subject_id']), name = "info_source_3")
infosource3.iterables = [('subject_id', subject_list)]

infosource4 = Node(IdentityInterface(fields=['subject_id']), name = "info_source_4")
infosource4.iterables = [('subject_id', subject_list)]

infosource5 = Node(IdentityInterface(fields=['subject_id']), name = "info_source_5")
infosource5.iterables = [('subject_id', subject_list)]

infosource6 = Node(IdentityInterface(fields=['subject_id']), name = "info_source_6")
infosource6.iterables = [('subject_id', subject_list)]

infosource7 = Node(IdentityInterface(fields=['subject_id']), name = "info_source_7")
infosource7.iterables = [('subject_id', subject_list)]

infosource8 = Node(IdentityInterface(fields=['subject_id']), name = "info_source_8")
infosource8.iterables = [('subject_id', subject_list)]

infosource9 = Node(IdentityInterface(fields=['subject_id']), name = "info_source_9")
infosource9.iterables = [('subject_id', subject_list)]

infosource10 = Node(IdentityInterface(fields=['subject_id']), name = "info_source_10")
infosource10.iterables = [('subject_id', subject_list)]

# create templates
lhtemplate_files = opj(datadir,'sub-102-lhtemplate[0, 1, 2].nii.gz')
mi_files = opj(datadir,'*{subject_id}*.lh.hippoSfLabels-T1.long.v10.nii.gz')
#nonbinarized_labels = opj(datadir,'l{subject_id}_hrlab_nonbin.nii.gz')

new_template_files = opj(datadir,'normflow/_index_[0,1,2]/mri_convert/average_out.nii.gz')
new_template_files_2 = opj(datadir,'normflow2/_index_[0,1,2]/mri_convert_2/average_out.nii.gz')
new_template_files_3 = opj(datadir,'normflow3/_index_[0,1,2]/mri_convert_3/average_out.nii.gz')
new_template_files_4 = opj(datadir,'normflow4/_index_[0,1,2]/mri_convert_4/average_out.nii.gz')
new_template_files_5 = opj(datadir,'normflow5/_index_[0,1,2]/mri_convert_5/average_out.nii.gz')
new_template_files_6 = opj(datadir,'normflow6/_index_[0,1,2]/mri_convert_6/average_out.nii.gz')
new_template_files_7 = opj(datadir,'normflow7/_index_[0,1,2]/mri_convert_7/average_out.nii.gz')
new_template_files_8 = opj(datadir,'normflow8/_index_[0,1,2]/mri_convert_8/average_out.nii.gz')
new_template_files_9 = opj(datadir,'normflow9/_index_[0,1,2]/mri_convert_9/average_out.nii.gz')

templates = {'lhtemplate': lhtemplate_files,
            'mi': mi_files,
            }

templates2 = {'mi': mi_files,
             'new_template': new_template_files,
            }

templates3 = {'mi': mi_files,
            'new_template_2': new_template_files_2,
            }

templates4 = {'mi': mi_files,
            'new_template_3': new_template_files_3,
            }

templates5 = {'mi': mi_files,
            'new_template_4': new_template_files_4,
            }

templates6 = {'mi': mi_files,
            'new_template_5': new_template_files_5,
            }

templates7 = {'mi': mi_files,
            'new_template_6': new_template_files_6,
            }

templates8 = {'mi': mi_files,
            'new_template_7': new_template_files_7,
            }

templates9 = {'mi': mi_files,
              'new_template_8': new_template_files_8,
             }

templates10 = {'mi': mi_files,
#               'nonbinarized_labels': nonbinarized_labels,
               'new_template_9': new_template_files_9,
             }
        
#select images organized by subject
selectfiles = Node(SelectFiles(templates, force_lists=['lhtemplate','mi'], 
                               sort_filelist = True, 
                               base_directory=datadir), 
                               name = "select_files")

selectfiles2 = Node(SelectFiles(templates2, force_lists=['mi', 'new_template'],
                               sort_filelist = True,
                               base_directory=datadir),
                               name = "select_files_2")

selectfiles3 = Node(SelectFiles(templates3, force_lists=['mi', 'new_template_2'],
                               sort_filelist = True,
                               base_directory=datadir),
                               name = "select_files_3")

selectfiles4 = Node(SelectFiles(templates4, force_lists=['mi', 'new_template_3'],
                               sort_filelist = True,
                               base_directory=datadir),
                               name = "select_files_4")

selectfiles5 = Node(SelectFiles(templates5, force_lists=['mi', 'new_template_4'],
                               sort_filelist = True,
                               base_directory=datadir),
                               name = "select_files_5")

selectfiles6 = Node(SelectFiles(templates6, force_lists=['mi', 'new_template_5'],
                               sort_filelist = True,
                               base_directory=datadir),
                               name = "select_files_6")

selectfiles7 = Node(SelectFiles(templates7, force_lists=['mi', 'new_template_6'],
                               sort_filelist = True,
                               base_directory=datadir),
                               name = "select_files_7")

selectfiles8 = Node(SelectFiles(templates8, force_lists=['mi', 'new_template_7'],
                               sort_filelist = True,
                               base_directory=datadir),
                               name = "select_files_8")

selectfiles9 = Node(SelectFiles(templates9, force_lists=['mi','new_template_8'],
                               sort_filelist = True,
                               base_directory=datadir),
                               name = "select_files_9")


#add in the nonbinarized labels here
selectfiles10 = Node(SelectFiles(templates10, force_lists=['mi', 'new_template_9'],
                               sort_filelist = True,
                               base_directory=datadir),
                               name = "select_files_10")

#datasink = Node(DataSink(base_directory= datadir, container = 'output_dir'), name = "datasink")
#substitutions = [('_subject_id_',''),
#                ]

#Replicates fwd transforms to match iterfield length and flatten nested list
def reptrans(forward_transforms):
    import numpy as np
    nested_list = np.ndarray.tolist(np.tile(forward_transforms,[1,3]))
    transforms = [val for sublist in nested_list for val in sublist]
    return transforms

#Flattens nested list
def flatten_nlist(out):
    return [val for sublist in out for val in sublist]

#Removes an element from list and then replicates the new list
def remove_second_element_reptrans(forward_transforms):
    import numpy as np
    forward_transforms = forward_transforms[0]
    nested_list = np.ndarray.tolist(np.tile(forward_transforms,[1,3]))
    transforms = [val for sublist in nested_list for val in sublist]
    return transforms

#Removes an element from list
def remove_first_element(forward_transforms):
    import numpy as np
    return forward_transforms[1]

#Returns first element from list
def return_first_element(output_image):
    import numpy as np
    return output_image[0]

# Create pipeline and connect nodes
workflow = Workflow(name='normflow')
workflow.base_dir = datadir
workflow.connect([
                (infosource, selectfiles, [('subject_id', 'subject_id')]),
                (selectfiles, antsreg_rigid, [('lhtemplate','fixed_image'),('mi','moving_image')]),
                (selectfiles, apply_rigid, [('lhtemplate','reference_image'),('mi','input_image')]),
                (antsreg_rigid, apply_rigid, [(('forward_transforms',reptrans),'transforms')]),
                (apply_rigid, sl, [('output_image', 'inlist')]),
                (sl, ml, [('out','in1')]),
                (ml, avg_rigid, [(('out', flatten_nlist),'images')]),
                (avg_rigid, mc, [('output_average_image','in_file')]),
                 ])

workflow2 = Workflow(name='normflow2')
workflow2.base_dir = datadir
workflow2.connect([
                (infosource2, selectfiles2, [('subject_id', 'subject_id')]),
                (selectfiles2, antsreg_rigid2, [('mi','moving_image'),('new_template','fixed_image')]),
                (selectfiles2, apply_rigid2, [('mi','input_image'),('new_template','reference_image')]),
                (antsreg_rigid2, apply_rigid2, [(('forward_transforms',reptrans,),'transforms')]),
                (apply_rigid2, sl2, [('output_image', 'inlist')]),
                (sl2, ml3, [('out','in1')]),
                (ml3, avg_rigid2, [(('out', flatten_nlist),'images')]),
                (avg_rigid2, mc2, [('output_average_image','in_file')]),
                ])

workflow3 = Workflow(name='normflow3')
workflow3.base_dir = datadir
workflow3.connect([
                (infosource3, selectfiles3, [('subject_id', 'subject_id')]),
                (selectfiles3, antsreg_rigid3, [('mi','moving_image'),('new_template_2','fixed_image')]),
                (selectfiles3, apply_rigid3, [('mi','input_image'),('new_template_2','reference_image')]),
                (antsreg_rigid3, apply_rigid3, [(('forward_transforms',reptrans,),'transforms')]),
                (apply_rigid3, sl3, [('output_image', 'inlist')]),
                (sl3, ml4, [('out','in1')]),
                (ml4, avg_rigid3, [(('out', flatten_nlist),'images')]),
                (avg_rigid3, mc3, [('output_average_image','in_file')]),
                ])

workflow4 = Workflow(name='normflow4')
workflow4.base_dir = datadir
workflow4.connect([
                (infosource4, selectfiles4, [('subject_id', 'subject_id')]),
                (selectfiles4, antsreg_affine1, [('mi','moving_image'),('new_template_3','fixed_image')]),
                (selectfiles4, apply_affine1, [('mi','input_image'),('new_template_3','reference_image')]),
                (antsreg_affine1, apply_affine1, [(('forward_transforms',reptrans,),'transforms')]),
                (apply_affine1, sl4, [('output_image', 'inlist')]),
                (sl4, ml5, [('out','in1')]),
                (ml5, avg_affine1, [(('out', flatten_nlist),'images')]),
                (avg_affine1, mc4, [('output_average_image','in_file')]),
                ])

workflow5 = Workflow(name='normflow5')
workflow5.base_dir = datadir
workflow5.connect([
                (infosource5, selectfiles5, [('subject_id', 'subject_id')]),
                (selectfiles5, antsreg_affine2, [('mi','moving_image'),('new_template_4','fixed_image')]),
                (selectfiles5, apply_affine2, [('mi','input_image'),('new_template_4','reference_image')]),
                (antsreg_affine2, apply_affine2, [(('forward_transforms',reptrans,),'transforms')]),
                (apply_affine2, sl5, [('output_image', 'inlist')]),
                (sl5, ml6, [('out','in1')]),
                (ml6, avg_affine2, [(('out', flatten_nlist),'images')]),
                (avg_affine2, mc5, [('output_average_image','in_file')]),
                ])

workflow6 = Workflow(name='normflow6')
workflow6.base_dir = datadir
workflow6.connect([
                (infosource6, selectfiles6, [('subject_id', 'subject_id')]),
                (selectfiles6, antsreg_BSpline1, [('mi','moving_image'),('new_template_5','fixed_image')]),
                (selectfiles6, apply_BSpline1, [('mi','input_image'),('new_template_5','reference_image')]),
                (antsreg_BSpline1, apply_BSpline1, [(('composite_transform',reptrans,),'transforms')]),
                (apply_BSpline1, sl6, [('output_image', 'inlist')]),
                (sl6, ml7, [('out','in1')]),
                (ml7, avg_BSpline1, [(('out', flatten_nlist),'images')]),
                (avg_BSpline1, mc6, [('output_average_image','in_file')]),
                ])

workflow7 = Workflow(name='normflow7')
workflow7.base_dir = datadir
workflow7.connect([
                (infosource7, selectfiles7, [('subject_id', 'subject_id')]),
                (selectfiles7, antsreg_BSpline2, [('mi','moving_image'),('new_template_6','fixed_image')]),
                (selectfiles7, apply_BSpline2, [('mi','input_image'),('new_template_6','reference_image')]),
                (antsreg_BSpline2, apply_BSpline2, [(('composite_transform',reptrans,),'transforms')]),
                (apply_BSpline2, sl7, [('output_image', 'inlist')]),
                (sl7, ml8, [('out','in1')]),
                (ml8, avg_BSpline2, [(('out', flatten_nlist),'images')]),
                (avg_BSpline2, mc7, [('output_average_image','in_file')]),
                ])

workflow8 = Workflow(name='normflow8')
workflow8.base_dir = datadir
workflow8.connect([
                (infosource8, selectfiles8, [('subject_id', 'subject_id')]),
                (selectfiles8, antsreg_BSpline3, [('mi','moving_image'),('new_template_7','fixed_image')]),
                (selectfiles8, apply_BSpline3, [('mi','input_image'),('new_template_7','reference_image')]),
                (antsreg_BSpline3, apply_BSpline3, [(('composite_transform',reptrans,),'transforms')]),
                (apply_BSpline3, sl8, [('output_image', 'inlist')]),
                (sl8, ml9, [('out','in1')]),
                (ml9, avg_BSpline3, [(('out', flatten_nlist),'images')]),
                (avg_BSpline3, mc8_test, [('output_average_image','in_file')]),
                ])

workflow9 = Workflow(name='normflow9')
workflow9.base_dir = datadir
workflow9.connect([
                (infosource9, selectfiles9, [('subject_id', 'subject_id')]),
                (selectfiles9, antsreg_BSpline4, [('mi','moving_image'),('new_template_8','fixed_image')]),
                (selectfiles9, apply_BSpline4, [('mi','input_image'),('new_template_8','reference_image')]),
                (antsreg_BSpline4, apply_BSpline4, [(('composite_transform',reptrans,),'transforms')]),
                (apply_BSpline4, sl9, [('output_image', 'inlist')]),
                (sl9, ml10, [('out','in1')]),
                (ml10, avg_BSpline4, [(('out', flatten_nlist),'images')]),
                (avg_BSpline4, mc9, [('output_average_image','in_file')]),
                ])


#Test the transform on the non-binarized labels

workflow10 = Workflow(name='normflow10')
workflow10.base_dir = datadir
workflow10.connect([
                (infosource10, selectfiles10, [('subject_id', 'subject_id')]),
                (selectfiles10, antsreg_BSpline4, [('mi','moving_image'),('new_template_9','fixed_image')]),
                (selectfiles10, apply_BSpline5, [('nonbinarized_labels','input_image')]),
                (antsreg_BSpline4, apply_BSpline5, [('composite_transform','transforms')]),
                (apply_BSpline5, sl10, [('output_image','inlist')]),
                (sl10, ml11, [('out','in1')]),
                (ml11, avg_BSpline5, [(('out', flatten_nlist),'images')]),
#need to flatten nlist?
                (avg_BSpline5, mc10, [('output_average_image','in_file')]),
                ])

workflow11 = Workflow(name='normflow11')
workflow11.base_dir = datadir
workflow11.connect([
                (infosource10, selectfiles10, [('subject_id', 'subject_id')]),
                (selectfiles10, antsreg_BSpline4a, [('mi','moving_image'),('new_template_9','fixed_image')]),
                (selectfiles10, apply_BSpline4a, [('mi','input_image'),('new_template_9','reference_image')]),
                (antsreg_BSpline4a, apply_BSpline4a, [(('composite_transform',reptrans,),'transforms')]),
                (apply_BSpline4a, jacobian, [(('output_image', return_first_element),'deformationField')]),
                ])

#visualize workflow; makes graph with everything and simplified one
# import pydotplus
# workflow.write_graph(graph2use='exec',format='png')
# workflow.write_graph(graph2use='colored',format='png')

# workflow2.write_graph(graph2use='exec',format='png')
# workflow2.write_graph(graph2use='colored',format='png')

# workflow3.write_graph(graph2use='exec',format='png')
# workflow3.write_graph(graph2use='colored',format='png')

# workflow4.write_graph(graph2use='exec',format='png')
# workflow4.write_graph(graph2use='colored',format='png')
 
# workflow5.write_graph(graph2use='exec',format='png')
# workflow5.write_graph(graph2use='colored',format='png')

# workflow6.write_graph(graph2use='exec',format='png')
# workflow6.write_graph(graph2use='colored',format='png')

# workflow7.write_graph(graph2use='exec',format='png')
# workflow7.write_graph(graph2use='colored',format='png')

# workflow8.write_graph(graph2use='exec',format='png')
# workflow8.write_graph(graph2use='colored',format='png')

# workflow9.write_graph(graph2use='exec',format='png')
# workflow9.write_graph(graph2use='colored',format='png')

# workflow10.write_graph(graph2use='exec',format='png')
# workflow10.write_graph(graph2use='colored',format='png')

# workflow11.write_graph(graph2use='exec',format='png')
# workflow11.write_graph(graph2use='colored',format='png')

# Run the workflow

workflow.run(plugin='SLURM', plugin_args={'jobid_re': '([0-9]*)',
                                          'sbatch_args': '--cpus-per-task=16 --mem=64g --time=8:00:00'
                                          })

workflow2.run(plugin='SLURM', plugin_args={'jobid_re': '([0-9]*)',
                                           'sbatch_args': '--cpus-per-task=16 --mem=64g --time=8:00:00'
                                          })

workflow3.run(plugin='SLURM', plugin_args={'jobid_re': '([0-9]*)',
                                           'sbatch_args': '--cpus-per-task=16 --mem=64g --time=8:00:00'
                                          })

workflow4.run(plugin='SLURM', plugin_args={'jobid_re': '([0-9]*)',
                                          'sbatch_args': '--cpus-per-task=16 --mem=64g --time=8:00:00'
                                        })

workflow5.run(plugin='SLURM', plugin_args={'jobid_re': '([0-9]*)',
                                          'sbatch_args': '--cpus-per-task=16 --mem=64g --time=8:00:00'
                                        })

workflow6.run(plugin='SLURM', plugin_args={'jobid_re': '([0-9]*)',
                                          'sbatch_args': '--cpus-per-task=16 --mem=64g --time=24:00:00'
                                        })

workflow7.run(plugin='SLURM', plugin_args={'jobid_re': '([0-9]*)',
                                          'sbatch_args': '--cpus-per-task=16 --mem=64g --time=24:00:00'
                                        })

workflow8.run(plugin='SLURM', plugin_args={'jobid_re': '([0-9]*)',
                                          'sbatch_args': '--cpus-per-task=16 --partition=norm --mem=64g --time=24:00:00'
                                        })

workflow9.run(plugin='SLURM', plugin_args={'jobid_re': '([0-9]*)',
                                          'sbatch_args': '--cpus-per-task=16 --partition=norm --mem=64g --time=24:00:00'
                                        })

# workflow10.run(plugin='SLURM', plugin_args={'jobid_re': '([0-9]*)',
#                                           'sbatch_args': '--cpus-per-task=8 --mem=64g --time=24:00:00'
#                                           })

workflow11.run(plugin='SLURM', plugin_args={'jobid_re': '([0-9]*)',
                                          'sbatch_args': '--cpus-per-task=16 --partition=norm --mem=64g --time=24:00:00'
                                        })

