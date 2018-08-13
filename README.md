# Longitudinal tensor-based morphometry - ketamine's effects on hippocampal subfield structure in major depressive disorder

## Pre-processing
### Subject-level templates & deformation field from scan to subject
#### Working directory: /gpfs/gsfs6/users/Hippo_hr/moa/anal/TBM
1. Convert hippocampus labels in .mgz to .nii.gz. Prepare a list of labels and target paths with full filepaths. Modify and use convert_to_nifti.sh to generate bash script, convert_labels.sh, to copy over. Labels in .mgz are in /gpfs/gsfs6/users/Hippo_hr/moa/derivatives/fs_subj_expert_opts.
2. Run bias-field correction on T1-w image, dilate the Freesurfer labels, mask T1-w image with the dilated label,  and generate crude initial templates (will need to create a padded image in subject space to create template: pad.sh): bfc.sh, dil.sh, mask.sh, binarize_labels.sh, create_init_templates.sh
3. Generate python nipype scripts for each subject's left hippocampus: modify_script.sh
4. Print and run nipype pipelines to be run: proc.sh
5. Repeat 3 to 4 for right hippocampus. 

Utility scripts:
findIncomplete.sh: run in data directory to find list of files without complete 11 workflows

Notes: subject 113 and 325 excluded (same as in cleaned clinical data)

### Group-level templates & deformation field from subject template to group template
1. Using final templates for each subject, create group level template for patients and controls. First, use create_group_templates.sh to average subject level templates to new initial crude label and T1-w templates:
```*normflow9/_index_[0,1]/mri_convert_9/average_out.nii.gz```
Apply pipeline, ants_test_slurm_group.ipynb, with new crude initial templates and subject level templates as the inputs (use symlinkSubjTemplates.sh for input file paths), to create new group templates as the outputs.
2. Apply transform/deformation field from subject-group template to the deformation field from scansession-subject template. This will incorporate population features for enhanced cross-subject validity and group comparison. Use repTransforms.sh to symlink the 54 subject-group transforms and then duplicate each by the different numbers of scan sessions. Use subjectToGroupApplyTransforms.sh to generate swarm command to apply transforms to corresponding deformation fields.
Scan-subject deformation field
```*normflow11/_subject_id*/jacobian/jacobian.nii.gz```

Excluded sessions: 102/0203; 108/0525; 308/0620 (same as in cleaned clinical data)

## Analysis

### Percent change maps

A la Gogtay et al and ADNI methods, percent change can be represented by Jacobian = 1 - f, and f x 100.

Subjects with 1 baseline (b) and at follow-up timepoints (f):

1. 32 patients, 18 controls
2. 30 patients, 14 controls
3. 26 patients, 9 controls
4. 21 patients, 8 controls

Percent change is calculated by subtracting the group-corrected Jacobian fields with the baseline as reference: f1-b, f2-b, f3-b, and f4-b. Cross over design, so subjects are their own controls for drug effects. Sort by day and type (b, p2, p10, k2, k10) depending on crossover order.

### Permutation testing

1. Using FSL's randomise, permute the session-to-subject level jacobian fields for group and drug. 
2. Perform t-tests to assess differences between groups
3. Assess the correlation between hippocampal subfield deformation in patients and clinical measures.

### Doing
1. Percent change maps for left hippo.
2. Attempting solutions for I/O SLURM problem

### To do
1. Subject level templates for right hippocampus.
2. modify rest of r-HPC scripts for the workflow.run commands

### Issues // attempted solution

1. socket i/o timeout -- doubling walltime
2. socket i/o timeout -- update to current nipype version, switch to py3.5, remove terminal output 'file', stop debug messages (save i/o load?)
3. socket i/o timout -- output to scratch (non-NFS mounted drive)
4. socket i/o timeout -- clean working directories