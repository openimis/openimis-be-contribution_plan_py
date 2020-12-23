# openIMIS Backend Contribution Plan reference module
This repository holds the files of the openIMIS Backend ContributionPlan and ContributionPlanBundle reference module.
It is dedicated to be deployed as a module of [openimis-be_py](https://github.com/openimis/openimis-be_py).

## ORM mapping:
* tblContributionPlanBundle > ContributionPlanBundle
* tblContributionPlan > ContributionPlan
* tblContributionPlanBundleDetails > ContributionPlanBundleDetails

## GraphQl Queries
* contributionPlanBundle 
* contributionPlan
* contributionPlanBundleDetails

## GraphQL Mutations - each mutation emits default signals and return standard error lists (cfr. openimis-be-core_py)
* createContributionPlanBundle
* updateContributionPlanBundle
* deleteContributionPlanBundle
* replaceContributionPlanBundle
* createContributionPlan
* updateContributionPlan
* deleteContributionPlan
* replaceContributionPlan
* createContributionPlanBundleDetails
* updateContributionPlanBundleDetails
* deleteContributionPlanBundleDetails

## Services
ContributionPlanBundle, CRUD services, replace
ContributionPlan - CRUD services, replace
ContributionPlanBundleDetails - create, update, delete

## Configuration options (can be changed via core.ModuleConfiguration)