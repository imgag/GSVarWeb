# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
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


