# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 0.0.6 - 29.07.2019
### Added
- Make it possible to rate variants yourself in the frontend
- Display gchboc rating in table

### Changed
- Dont use ratings - use classifications @marc-sturm
- Changed title to GSVarWeb for GCHBOC
- Correctly insert records so they will not be overriden if they arent the same
- Automatically reload annotated file when rating
- Always download annotated file

## 0.0.5 - 29.07.2019
### Added
- Added controllers for rating variants.
- Added color for ClinVar and HGMD in ColumnDialog
- Add tooltip to ClinVar and HGMD
- Added Google link
- Added GnomAD link

### Changed
- Fix coloring at least for HGMD and ClinVar
- Make snackbars display permanently
- Remove caching everywhere

## 0.0.4
### Added
- Added logout button
- Add tooltip for all cells

### Changed
- Add development server to default CORS_ORIGIN
- Made ColumnDialog subheadings -> titles
- Split COSMIC entries by space
- Use subprocess to catch errors when filtering
- Split CORS_ORIGIN env variable

## 0.0.3
### Added
- Added download button
- Added netlify support

### Changed
- Rename REALM -> AUTH_REALM
- Rename NGS_BITS_BIN -> NGS_BITS
- Rename MEGSAP_DIR -> MEGSAP
- Rename VUE_APP_BASEPATH -> VUE_APP_API_URL
- Rename NGS_BITS_DATA -> DATA
- Change way of handling origins variable
- Removed v-data-table with ag-grid
- Rename GSVar -> GSvar everywhere
- Split GeneSplicer by &
- Add better error message when filter fails
- Break COSMIC into multiple links using ,
- Changed default realm to debug
- Changed default display limit for variants in column dialog to 15
- Removed apply filter button -> automatically load filter when changing
- Use user (id) as base name for storing files
- Rename ID -> Transcript
- Remove the "exon" part from the exon string on display
- Use createObjectURL to download files with JWT

### Removed
- Removed unauthenticated access in debug config

## 0.0.2

### Changed
- better error handling with detail from request body
- better detail modal like in GSVar
- renamed GSVar -> GSvar
- make table columns uniform
- don't use the VariantFilterRequest model in the controller anymore

## 0.0.1

### Added 
- add OpenAPI-based API
- serve vcf2gsvar and an_vep (megSAP) via API
- serve VcfFilterAnnotate via API
- add multi-stage UI (log in, select file, select filter)
- automatically annotate (using an_vep) and convert (using vcf2gsvar) VCF files
- add linting for frontend and API
- add tests for API


