If not exists(Select 1 from sysindexes where name = 'IX_FileFormatID') CREATE INDEX [IX_FileFormatID] ON [dbo].[omFile]([FileFormatId]) ON [PRIMARY]

If not exists(Select 1 from sysindexes where name = 'IX_MaxIssueLevel') CREATE INDEX [IX_MaxIssueLevel] ON [dbo].[omFile] ([MaxIssueLevel])

If not exists(Select 1 from sysindexes where name = 'IX_Extension') CREATE INDEX [IX_Extension] ON [dbo].[omFile] ([Extension])

If not exists(Select 1 from sysindexes where name = 'IX_DNS') CREATE  INDEX [IX_DNS] ON [dbo].[omFile] ([DNS])

If not exists(Select 1 from sysindexes where name = 'IX_ComputerName') CREATE  INDEX [IX_ComputerName] ON [dbo].[omFile] ([ComputerName])

If not exists(Select 1 from sysindexes where name = 'IX_ModifiedDate') CREATE  INDEX [IX_ModifiedDate] ON [dbo].[omFile] ([ModifiedDate])

If not exists(Select 1 from sysindexes where name = 'IX_IssueId_IsResolved') CREATE INDEX [IX_IssueId_IsResolved] ON [dbo].[omFileIssue]([IssueId], [IsResolved]) ON [PRIMARY]

If not exists(Select 1 from sysindexes where name = 'IX_omAction_ToolId') create nonclustered index [IX_omAction_ToolId] on omAction([ToolId])
If not exists(Select 1 from sysindexes where name = 'IX_omActionIssue_IssueId') create nonclustered index [IX_omActionIssue_IssueId] on omActionIssue([IssueId])
If not exists(Select 1 from sysindexes where name = 'IX_omActionIssue_ToolId') create nonclustered index [IX_omActionIssue_ToolId] on omActionIssue([ToolId])
If not exists(Select 1 from sysindexes where name = 'IX_omFile_CSIDL') create nonclustered index [IX_omFile_CSIDL] on omFile([CSIDL])
If not exists(Select 1 from sysindexes where name = 'IX_omFileScanFile_ScanFileId') create nonclustered index [IX_omFileScanFile_ScanFileId] on omFileScanFile([ScanFileId])
If not exists(Select 1 from sysindexes where name = 'IX_omIssue_IssueLevelId') create nonclustered index [IX_omIssue_IssueLevelId] on omIssue([IssueLevelId])
If not exists(Select 1 from sysindexes where name = 'IX_omIssue_IssueTypeId') create nonclustered index [IX_omIssue_IssueTypeId] on omIssue([IssueTypeId])
If not exists(Select 1 from sysindexes where name = 'IX_omToolIssue_IssueId') create nonclustered index [IX_omToolIssue_IssueId] on omToolIssue([IssueId])
If not exists(Select 1 from sysindexes where name = 'IX_osError_ErrorID') create nonclustered index [IX_osError_ErrorID] on osError([ErrorID])
If not exists(Select 1 from sysindexes where name = 'IX_osError_ScanFileID') create nonclustered index [IX_osError_ScanFileID] on osError([ScanFileID])
If not exists(Select 1 from sysindexes where name = 'IX_osError_ScanID') create nonclustered index [IX_osError_ScanID] on osError([ScanID])
If not exists(Select 1 from sysindexes where name = 'IX_osScanFile_CSIDL') create nonclustered index [IX_osScanFile_CSIDL] on osScanFile([CSIDL])
If not exists(Select 1 from sysindexes where name = 'IX_osScanFile_FileFormatID') create nonclustered index [IX_osScanFile_FileFormatID] on osScanFile([FileFormatID])
If not exists(Select 1 from sysindexes where name = 'IX_osScanFile_ScanID') create nonclustered index [IX_osScanFile_ScanID] on osScanFile([ScanID])
If not exists(Select 1 from sysindexes where name = 'IX_AccessProperties_AccessVersion') create nonclustered index [IX_AccessProperties_AccessVersion] on AccessProperties([AccessVersion])
If not exists(Select 1 from sysindexes where name = 'IX_AccessProperties_IsSample') create nonclustered index [IX_AccessProperties_IsSample] on AccessProperties([IsSample])
If not exists(Select 1 from sysindexes where name = 'IX_AccessProperties_IsSystem') create nonclustered index [IX_AccessProperties_IsSystem] on AccessProperties([IsSystem])
If not exists(Select 1 from sysindexes where name = 'IX_AccessProperties_IsBackup') create nonclustered index [IX_AccessProperties_IsBackup] on AccessProperties([IsBackup])
If not exists(Select 1 from sysindexes where name = 'IX_AccessProperties_IsOld') create nonclustered index [IX_AccessProperties_IsOld] on AccessProperties([IsOld])
If not exists(Select 1 from sysindexes where name = 'IX_omAccessRatings_RatingID') create nonclustered index [IX_omAccessRatings_RatingID] on omAccessRatings([RatingID])

go