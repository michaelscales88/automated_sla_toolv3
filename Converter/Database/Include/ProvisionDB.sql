SET NOCOUNT ON
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

/****** Object:  Table [dbo].[AccessDatabasesRatingProperties]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessDatabasesRatingProperties](
	[RatingID] [tinyint] NOT NULL,
	[Rating] [nvarchar](50) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_AccessDatabasesRatingProperties] PRIMARY KEY CLUSTERED 
(
	[RatingID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/*This table contains data on the status of import processes */
Create table [dbo].[Process_Control] (
	[ComputerName] nvarchar(50), 
	[ImportInProgress] bit, 
	[TimeStarted] datetime)
go

/*Insert a default record into this table*/
insert Process_Control values('', 0, getdate())
go

/****** Object:  Table [dbo].[AccessFields]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessFields](
	[FileID] [uniqueidentifier] NOT NULL,
	[TableName] [nvarchar](64) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[FieldName] [nvarchar](64) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[FieldType] [tinyint] NOT NULL,
 CONSTRAINT [PK_AccessFields] PRIMARY KEY CLUSTERED 
(
	[FileID] ASC,
	[TableName] ASC,
	[FieldName] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[AccessFieldTypeLookupProperties]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessFieldTypeLookupProperties](
	[FieldType] [tinyint] NOT NULL,
	[FieldTypeFriendlyName] [nvarchar](64) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_AccessFieldTypeLookupProperties] PRIMARY KEY CLUSTERED 
(
	[FieldType] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[AccessForms]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessForms](
	[FileID] [uniqueidentifier] NOT NULL,
	[FormName] [nvarchar](64) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_AccessForms] PRIMARY KEY CLUSTERED 
(
	[FileID] ASC,
	[FormName] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[AccessIssuesProperties]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessIssuesProperties](
	[IssueId] [tinyint] NOT NULL,
	[IssueText] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[UserIntervention] [nvarchar](50) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[IssueType] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[UserInterventionPriority] [tinyint] NOT NULL,
 CONSTRAINT [PK_AccessIssuesProperties] PRIMARY KEY CLUSTERED 
(
	[IssueId] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[AccessMacros]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessMacros](
	[FileID] [uniqueidentifier] NOT NULL,
	[MacroName] [nvarchar](64) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_AccessMacros] PRIMARY KEY CLUSTERED 
(
	[FileID] ASC,
	[MacroName] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[AccessModules]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessModules](
	[FileID] [uniqueidentifier] NOT NULL,
	[ModuleName] [nvarchar](64) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_AccessModules] PRIMARY KEY CLUSTERED 
(
	[FileID] ASC,
	[ModuleName] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

Create table dbo.AccessSampleFiles(
	[Name] nvarchar(255) not null,
CONSTRAINT [PK_AccessSampleFiles] PRIMARY KEY CLUSTERED 
(
	[Name] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

Create table dbo.AccessBackupTokens(
	[Name] nvarchar(255) not null,
CONSTRAINT [PK_AccessBackupTokens] PRIMARY KEY CLUSTERED 
(
	[Name] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

Create table dbo.AccessSystemFiles(
	[Name] nvarchar(255) not null,
CONSTRAINT [PK_AccessSystemFiles] PRIMARY KEY CLUSTERED 
(
	[Name] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

Create table dbo.AccessSettings(
	[SettingName] nvarchar(50) Not Null,
	[DateValue]	datetime,
CONSTRAINT [PK_AccessSettings] PRIMARY KEY CLUSTERED 
(
	[SettingName] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO	

Insert dbo.AccessSettings values('OldDate', '1/1/2000')
go

Create table dbo.omAccessIssue(
	[FileID] int not null,
	[IssueId] tinyint not null,
CONSTRAINT [PK_omAccessIssue] PRIMARY KEY CLUSTERED 
(
	[FileID],
	[IssueId] 
) ON [PRIMARY]
) ON [PRIMARY]
GO

Create table dbo.omAccessRatings(
	[FileID] int not null,
	[RatingId] tinyint not null,
CONSTRAINT [PK_omAccessRatings] PRIMARY KEY CLUSTERED 
(
	[FileID]
) ON [PRIMARY]
) ON [PRIMARY]
GO

Create table dbo.AccessReservedWords(
	[Name] nvarchar(50) not null,
CONSTRAINT [PK_AccessReservedWords] PRIMARY KEY CLUSTERED 
(
	[Name] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

Insert AccessReservedWords values('application')
Insert AccessReservedWords values('assistant')
Insert AccessReservedWords values('commandbars')
Insert AccessReservedWords values('docmd')
Insert AccessReservedWords values('forms')
Insert AccessReservedWords values('modules')
Insert AccessReservedWords values('references')
Insert AccessReservedWords values('reports')
Insert AccessReservedWords values('screen')
go


/****** Object:  Table [dbo].[AccessProperties]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessProperties](
	[FileID] [uniqueidentifier] NOT NULL,
	[ScanID] [uniqueidentifier] NOT NULL,
	[TableCount] [int] NULL,
	[QueryCount] [int] NULL,
	[FormCount] [int] NULL,
	[ReportCount] [int] NULL,
	[MacroCount] [int] NULL,
	[ModuleCount] [int] NULL,
	[ReferenceCount] [int] NULL,
	[CollatingOrder] [int] NULL,
	[Version] [nvarchar](5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[ReplicaID] [uniqueidentifier] NULL,
	[DesignMasterID] [uniqueidentifier] NULL,
	[ANSIQueryMODE] [bit] NULL,
	[AccessVersion] [nvarchar](40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[Build] [nvarchar](5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[ProjVer] [nvarchar](5) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[StartupForm] [nvarchar](64) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[NoConvertDialog] [bit] NULL,
	[DatabaseOwner] [nvarchar](64) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[IsCompiled] [bit] NULL,
	[IsSample] [bit] NULL,
	[IsBackup] [bit] NULL,
	[IsOld] [bit] NULL,
	[IsSystem] [bit] NULL,
 CONSTRAINT [PK_AccessProperties] PRIMARY KEY CLUSTERED 
(
	[FileID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[AccessQueries]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessQueries](
	[FileID] [uniqueidentifier] NOT NULL,
	[QueryName] [nvarchar](64) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[SQL] [ntext] COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[Connect] [ntext] COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[Type] [tinyint] NULL,
 CONSTRAINT [PK_AccessQueries] PRIMARY KEY CLUSTERED 
(
	[FileID] ASC,
	[QueryName] ASC
) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

/****** Object:  Table [dbo].[AccessQueriesTypeLookupProperties]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessQueriesTypeLookupProperties](
	[TypeID] [tinyint] NOT NULL,
	[TypeFriendlyName] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_AccessQueriesTypeLookupProperties] PRIMARY KEY CLUSTERED 
(
	[TypeID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[AccessReferences]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessReferences](
	[FileID] [uniqueidentifier] NOT NULL,
	[ReferenceName] [nvarchar](260) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[GUID] [uniqueidentifier] NULL,
	[FullPath] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[IsBroken] [bit] NULL,
	[Kind] [nvarchar](50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[Major] [int] NULL,
	[Minor] [int] NULL,
 CONSTRAINT [PK_AccessReferences] PRIMARY KEY CLUSTERED 
(
	[FileID] ASC,
	[ReferenceName] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[AccessReports]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessReports](
	[FileID] [uniqueidentifier] NOT NULL,
	[ReportName] [nvarchar](64) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_AccessReports] PRIMARY KEY CLUSTERED 
(
	[FileID] ASC,
	[ReportName] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[AccessTables]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessTables](
	[FileID] [uniqueidentifier] NOT NULL,
	[TableName] [nvarchar](64) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[RecordCount] [int] NULL,
	[Connect] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
 CONSTRAINT [PK_AccessTables] PRIMARY KEY CLUSTERED 
(
	[FileID] ASC,
	[TableName] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[AccessVersionsProperties]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[AccessVersionsProperties](
	[VersionCode] [nvarchar](40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[Version] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_AccessVersionsProperties] PRIMARY KEY CLUSTERED 
(
	[VersionCode] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[omAction]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omAction](
	[FileId] [int] NOT NULL,
	[ToolId] [int] NOT NULL,
	[ActionDate] [datetime] NOT NULL,
	[ActionOptions] [nvarchar](48) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[FileModifiedDate] [datetime] NULL,
 CONSTRAINT [PK_Action] PRIMARY KEY CLUSTERED 
(
	[FileId] ASC,
	[ToolId] ASC,
	[ActionDate] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[omActionFile]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omActionFile](
	[FileId] [int] NOT NULL,
	[ToolId] [int] NOT NULL,
	[ActionDate] [datetime] NOT NULL,
	[FileCategoryId] [int] NOT NULL,
	[Name] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[Path] [nvarchar](2048) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[ComputerName] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[Domain] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[omActionIssue]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omActionIssue](
	[FileId] [int] NOT NULL,
	[ToolId] [int] NOT NULL,
	[ActionDate] [datetime] NOT NULL,
	[IssueId] [int] NOT NULL,
	[IsResolved] [bit] NOT NULL,
	[PostStatus] [int] NULL,
	[PostDate] [datetime] NULL,
 CONSTRAINT [PK_ActionIssue] PRIMARY KEY CLUSTERED 
(
	[FileId] ASC,
	[ToolId] ASC,
	[ActionDate] ASC,
	[IssueId] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[omCSIDL]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omCSIDL](
	[CSIDL] [int] NOT NULL,
	[Name] [nvarchar](48) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_omCSIDL] PRIMARY KEY CLUSTERED 
(
	[CSIDL] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[omFile]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omFile](
	[FileId] [int] IDENTITY(1,1) NOT NULL,
	[LastScanFileId] [uniqueidentifier] NOT NULL,
	[Name] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[Path] [nvarchar](2048) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[ShortPath] [nvarchar](1024) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[Extension] [nvarchar](16) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[FileFormatId] [tinyint] NULL,
	[Size] [int] NULL,
	[CreatedDate] [datetime] NULL,
	[ModifiedDate] [datetime] NULL,
	[Owner] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[UserContext] [nvarchar](48) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[ComputerName] [nvarchar](48) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[DNS] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[HashCode] [int] NULL,
	[CSIDL] [int] NULL,
	[MaxIssueLevel] [int] NULL,
	[IsReadOnly] [bit] NULL,
 CONSTRAINT [PK_File] PRIMARY KEY CLUSTERED 
(
	[FileId] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[omFileCategory]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omFileCategory](
	[FileCategoryId] [int] NOT NULL,
	[Description] [nvarchar](48) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
 CONSTRAINT [PK_FileCategory] PRIMARY KEY CLUSTERED 
(
	[FileCategoryId] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[omFileIssue]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omFileIssue](
	[FileId] [int] NOT NULL,
	[IssueId] [int] NOT NULL,
	[IssueDate] [datetime] NOT NULL,
	[IsResolved] [bit] NOT NULL,
 CONSTRAINT [PK_FileIssue] PRIMARY KEY CLUSTERED 
(
	[FileId] ASC,
	[IssueId] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO


/****** Object:  Table [dbo].[omFileScanFile]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omFileScanFile](
	[FileId] [int] NOT NULL,
	[ScanFileId] [uniqueidentifier] NOT NULL,
 CONSTRAINT [PK_FileScanFile] PRIMARY KEY CLUSTERED 
(
	[FileId] ASC,
	[ScanFileId] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[omFilter]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omFilter](
	[FilterId] [int] IDENTITY(1,1) NOT NULL,
	[Name] [nvarchar](48) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[SQLText] [nvarchar](3600) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[Advanced] [bit] NOT NULL,
 CONSTRAINT [PK_omFilter] PRIMARY KEY CLUSTERED 
(
	[FilterId] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[omIssue]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omIssue](
	[IssueId] [int] NOT NULL,
	[Title] [nvarchar](48) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[Description] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[HelpURL] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[IssueLevelId] [int] NOT NULL,
	[IssueTypeId] [int] NOT NULL,
 CONSTRAINT [PK_Issue] PRIMARY KEY CLUSTERED 
(
	[IssueId] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[omIssueLevel]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omIssueLevel](
	[IssueLevelId] [int] NOT NULL,
	[Description] [nvarchar](48) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_IssueLevel] PRIMARY KEY CLUSTERED 
(
	[IssueLevelId] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[omIssueType]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omIssueType](
	[IssueTypeId] [int] NOT NULL,
	[Description] [nvarchar](48) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[IsPromoted] [bit] NOT NULL,
 CONSTRAINT [PK_IssueType] PRIMARY KEY CLUSTERED 
(
	[IssueTypeId] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[omTool]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omTool](
	[ToolId] [int] NOT NULL,
	[Title] [nvarchar](48) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[Description] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[HelpURL] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[Version] [nvarchar](48) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
 CONSTRAINT [PK_Tool] PRIMARY KEY CLUSTERED 
(
	[ToolId] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[omToolIssue]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[omToolIssue](
	[ToolId] [int] NOT NULL,
	[IssueId] [int] NOT NULL,
 CONSTRAINT [PK_ToolIssue] PRIMARY KEY CLUSTERED 
(
	[ToolId] ASC,
	[IssueId] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[osError]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osError](
	[osErrorID] [int] Not Null Identity(1,1),
	[ScanID] [uniqueidentifier] NOT NULL,
	[ScanFileID] [uniqueidentifier] NULL,
	[ErrorID] [int] NOT NULL,
	[ErrorInfo] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
CONSTRAINT [PK_osError] PRIMARY KEY CLUSTERED 
(
	[osErrorID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[osErrorText]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osErrorText](
	[ErrorID] [int] NOT NULL,
	[ErrorDescription] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_ErrorText] PRIMARY KEY CLUSTERED 
(
	[ErrorID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[osExcelProperty]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osExcelProperty](
	[ScanFileID] [uniqueidentifier] NOT NULL,
	[FileOpenNotSupported] [bit] NULL,
	[FileSaveNotSupported] [bit] NULL,
	[WorkspaceFile] [bit] NULL,
	[HTMLSaved] [bit] NULL,
	[OWC9] [bit] NULL,
	[OWC10] [bit] NULL,
	[OWC11] [bit] NULL,
	[FileFormat] [nvarchar](40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[LastSavedVersion] [nvarchar](40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[EmbeddedDocs] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[WSSLinkedList] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[MSERedcords] [bit] NULL,
	[ErrorChecking] [bit] NULL,
	[AccessDBConnection] [int] NULL,
	[SharedWorkBook] [bit] NULL,
	[LinkedContent] [bit] NULL,
	[Charts] [int] NULL,
	[OfficeArtShapes] [bit] NULL,
	[ELFEnabled] [bit] NULL,
	[StandardList] [bit] NULL,
	[ATP] [bit] NULL,
	[RelationalPivot] [int] NULL,
	[OLAPPivot] [int] NULL,
	[CondFormat] [bit] NULL,
 CONSTRAINT [PK_ExcelProperty] PRIMARY KEY CLUSTERED 
(
	[ScanFileID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[osExcelPropertyLinked]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osExcelPropertyLinked](
	[ScanFileID] [uniqueidentifier] NOT NULL,
	[Link] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
 CONSTRAINT [PK_ExcelPropertyLinked] PRIMARY KEY CLUSTERED 
(
	[ScanFileID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[osFileFormat]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osFileFormat](
	[FileFormatID] [tinyint] NOT NULL,
	[Description] [nvarchar](48) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_FileFormatID] PRIMARY KEY CLUSTERED 
(
	[FileFormatID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[osPowerPointProperty]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osPowerPointProperty](
	[ScanFileID] [uniqueidentifier] NOT NULL,
	[hasSendForReviewData] [bit] NULL,
	[hasEmbeddings] [bit] NULL,
	[hasVBA] [bit] NULL,
	[hasMicrosoftScriptEditorData] [bit] NULL,
	[hasPresentationBroadcastData] [bit] NULL,
	[hasDocumentRoutingSlip] [bit] NULL,
	[hasPublishandSubscribeData] [bit] NULL,
	[hasLargeNumberofOLEObjects] [bit] NULL,
 CONSTRAINT [PK_PowerPointProperty] PRIMARY KEY CLUSTERED 
(
	[ScanFileID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[osScan]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osScan](
	[ScanID] [uniqueidentifier] NOT NULL,
	[RunID] [int] NOT NULL,
	[Description] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[DestinationPath] [nvarchar](2048) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[ScanMyDocuments] [bit] NOT NULL,
	[ScanDesktop] [bit] NOT NULL,
	[DeepScan] [bit] NOT NULL,
	[ComputerName] [nvarchar](40) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[UserName] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[DNS] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[OS] [nvarchar](40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[LCID] [nvarchar](10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[PhysicalMemory] [nvarchar](40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[ScanDAO] [bit] NOT NULL,
	[AccessScan] [bit] NOT NULL,
	[DisableConvDialog] [bit] NULL,
	[MaxCopyFileSize] [int] NULL,
	[TempPath] [nvarchar](1024) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
 CONSTRAINT [PK_Scan] PRIMARY KEY CLUSTERED 
(
	[ScanID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

CREATE UNIQUE INDEX [IX_Run_Comp_User_DNS] ON [dbo].[osScan]([RunID], [ComputerName], [UserName], [DNS]) ON [PRIMARY]
go

/****** Object:  Table [dbo].[osScanFile]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osScanFile](
	[ScanFileID] [uniqueidentifier] NOT NULL,
	[ScanID] [uniqueidentifier] NOT NULL,
	[FileName] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[FilePath] [nvarchar](2048) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[ShortFilePath] [nvarchar](1024
) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[FileSize] [int] NULL,
	[FileExtension] [nvarchar](10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[FileFormatID] [tinyint] NOT NULL,
	[CreatedDate] [datetime] NULL,
	[ModifiedDate] [datetime] NULL,
	[FileOwner] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[IsReadOnly] [bit] NOT NULL,
	[HashCode] [int] NOT NULL,
	[CSIDL] [int] NOT NULL,
 CONSTRAINT [PK_ScanFile] PRIMARY KEY CLUSTERED 
(
	[ScanFileID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[osScanIncludedFolder]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osScanIncludedFolder](
	[ScanID] [uniqueidentifier] NOT NULL,
	[FolderPath] [nvarchar](2048) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_ScanIncludedFolder] PRIMARY KEY CLUSTERED 
(
	[ScanID] ASC,
	[FolderPath] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[osScanExcludedFolder]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osScanExcludedFolder](
	[ScanID] [uniqueidentifier] NOT NULL,
	[FolderPath] [nvarchar](2048) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_ScanExcludedFolder] PRIMARY KEY CLUSTERED 
(
	[ScanID] ASC,
	[FolderPath] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[osScanMappedDrive]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osScanMappedDrive](
	[ScanID] [uniqueidentifier] NOT NULL,
	[DriveLetter] [nvarchar](1) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	[DrivePath] [nvarchar](2048) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
 CONSTRAINT [PK_ScanMappedDrive] PRIMARY KEY CLUSTERED 
(
	[ScanID] ASC,
	[DriveLetter] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[osScanSummary]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osScanSummary](
	[ScanID] [uniqueidentifier] NOT NULL,
	[StartDateTime] [datetime] NULL,
	[EndDateTime] [datetime] NULL,
	[NumFilesScanned] [int] NOT NULL,
	[NumLogFiles] [int] NOT NULL,
	[Recoveries] [int] NOT NULL,
 CONSTRAINT [PK_ScanSummary] PRIMARY KEY CLUSTERED 
(
	[ScanID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[osVBAProperty]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osVBAProperty](
	[ScanFileID] [uniqueidentifier] NOT NULL,
	[CertIssuedBy] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[CertIssuedTo] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[CertSerialNum] [nvarchar](40) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[CertValidFrom] [datetime] NULL,
	[CertValidTo] [datetime] NULL,
	[SigTimeStampSigningTime] [datetime] NULL,
	[SigTimeStampSignerName] [nvarchar](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
 CONSTRAINT [PK_VBAProperty] PRIMARY KEY CLUSTERED 
(
	[ScanFileID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[osWordProperty]    Script Date: 06/09/2006 10:23:14 ******/
CREATE TABLE [dbo].[osWordProperty](
	[ScanFileID] [uniqueidentifier] NOT NULL,
	[HaveVersions] [bit] NULL,
 CONSTRAINT [PK_WordProperty] PRIMARY KEY CLUSTERED 
(
	[ScanFileID] ASC
) ON [PRIMARY]
) ON [PRIMARY]
GO


ALTER TABLE [dbo].[AccessFields]  WITH CHECK ADD  CONSTRAINT [FK_AccessFields_ScanFile] FOREIGN KEY([FileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[AccessForms]  WITH CHECK ADD  CONSTRAINT [FK_AccessForms_ScanFile] FOREIGN KEY([FileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[AccessMacros]  WITH CHECK ADD  CONSTRAINT [FK_AccessMacros_ScanFile] FOREIGN KEY([FileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[AccessModules]  WITH CHECK ADD  CONSTRAINT [FK_AccessModules_ScanFile] FOREIGN KEY([FileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[AccessProperties]  WITH CHECK ADD  CONSTRAINT [FK_AccessProperties_ScanFile] FOREIGN KEY([FileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[AccessQueries]  WITH CHECK ADD  CONSTRAINT [FK_AccessQueries_ScanFile] FOREIGN KEY([FileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[AccessReferences]  WITH CHECK ADD  CONSTRAINT [FK_AccessReferences_ScanFile] FOREIGN KEY([FileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[AccessReports]  WITH CHECK ADD  CONSTRAINT [FK_AccessReports_ScanFile] FOREIGN KEY([FileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[AccessTables]  WITH CHECK ADD  CONSTRAINT [FK_TablesProperties_ScanFile] FOREIGN KEY([FileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[omAction]  WITH CHECK ADD  CONSTRAINT [FK_omAction_omFile] FOREIGN KEY([FileId])
REFERENCES [dbo].[omFile] ([FileId])
GO
ALTER TABLE [dbo].[omAction]  WITH CHECK ADD  CONSTRAINT [FK_omAction_omTool] FOREIGN KEY([ToolId])
REFERENCES [dbo].[omTool] ([ToolId])
GO
ALTER TABLE [dbo].[omActionFile]  WITH CHECK ADD  CONSTRAINT [FK_omActionFile_omFile] FOREIGN KEY([FileId])
REFERENCES [dbo].[omFile] ([FileId])
GO
ALTER TABLE [dbo].[omActionFile]  WITH CHECK ADD  CONSTRAINT [FK_omActionFile_omFileCategory] FOREIGN KEY([FileCategoryId])
REFERENCES [dbo].[omFileCategory] ([FileCategoryId])
GO
ALTER TABLE [dbo].[omActionFile]  WITH CHECK ADD  CONSTRAINT [FK_omActionFile_omTool] FOREIGN KEY([ToolId])
REFERENCES [dbo].[omTool] ([ToolId])
GO
ALTER TABLE [dbo].[omActionIssue]  WITH CHECK ADD  CONSTRAINT [FK_omActionIssue_omFile] FOREIGN KEY([FileId])
REFERENCES [dbo].[omFile] ([FileId])
GO
ALTER TABLE [dbo].[omActionIssue]  WITH CHECK ADD  CONSTRAINT [FK_omActionIssue_omIssue] FOREIGN KEY([IssueId])
REFERENCES [dbo].[omIssue] ([IssueId])
GO
ALTER TABLE [dbo].[omActionIssue]  WITH CHECK ADD  CONSTRAINT [FK_omActionIssue_omTool] FOREIGN KEY([ToolId])
REFERENCES [dbo].[omTool] ([ToolId])
GO
ALTER TABLE [dbo].[omFile]  WITH CHECK ADD  CONSTRAINT [FK_omFile_osFileFormat] FOREIGN KEY([FileFormatId])
REFERENCES [dbo].[osFileFormat] ([FileFormatID])
GO
ALTER TABLE [dbo].[omFile]  WITH CHECK ADD  CONSTRAINT [FK_omFile_omCSIDL] FOREIGN KEY([CSIDL])
REFERENCES [dbo].[omCSIDL] ([CSIDL])
GO
ALTER TABLE [dbo].[omFileIssue]  WITH NOCHECK ADD  CONSTRAINT [FK_omFileIssue_omFile] FOREIGN KEY([FileId])
REFERENCES [dbo].[omFile] ([FileId])
GO
ALTER TABLE [dbo].[omFileIssue] CHECK CONSTRAINT [FK_omFileIssue_omFile]
GO
ALTER TABLE [dbo].[omFileIssue]  WITH NOCHECK ADD  CONSTRAINT [FK_omFileIssue_omIssue] FOREIGN KEY([IssueId])
REFERENCES [dbo].[omIssue] ([IssueId])
GO
ALTER TABLE [dbo].[omFileIssue] CHECK CONSTRAINT [FK_omFileIssue_omIssue]
GO
ALTER TABLE [dbo].[omFileScanFile]  WITH CHECK ADD  CONSTRAINT [FK_omFileScanFile_omFile] FOREIGN KEY([FileId])
REFERENCES [dbo].[omFile] ([FileId])
GO
ALTER TABLE [dbo].[omFileScanFile]  WITH CHECK ADD  CONSTRAINT [FK_omFileScanFile_osScanFile] FOREIGN KEY([ScanFileId])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[omIssue]  WITH CHECK ADD  CONSTRAINT [FK_omIssue_omIssueLevel] FOREIGN KEY([IssueLevelId])
REFERENCES [dbo].[omIssueLevel] ([IssueLevelId])
GO
ALTER TABLE [dbo].[omIssue]  WITH CHECK ADD  CONSTRAINT [FK_omIssue_omIssueType] FOREIGN KEY([IssueTypeId])
REFERENCES [dbo].[omIssueType] ([IssueTypeId])
GO
ALTER TABLE [dbo].[omToolIssue]  WITH CHECK ADD  CONSTRAINT [FK_omToolIssue_omIssue] FOREIGN KEY([IssueId])
REFERENCES [dbo].[omIssue] ([IssueId])
GO
ALTER TABLE [dbo].[omToolIssue]  WITH CHECK ADD  CONSTRAINT [FK_omToolIssue_omTool] FOREIGN KEY([ToolId])
REFERENCES [dbo].[omTool] ([ToolId])
GO
ALTER TABLE [dbo].[osError]  WITH CHECK ADD  CONSTRAINT [FK_osError_osErrorText] FOREIGN KEY([ErrorID])
REFERENCES [dbo].[osErrorText] ([ErrorID])
GO
ALTER TABLE [dbo].[osError]  WITH NOCHECK ADD  CONSTRAINT [FK_osError_osScan] FOREIGN KEY([ScanID])
REFERENCES [dbo].[osScan] ([ScanID])
GO
ALTER TABLE [dbo].[osError] CHECK CONSTRAINT [FK_osError_osScan]
GO
ALTER TABLE [dbo].[osError]  WITH NOCHECK ADD  CONSTRAINT [FK_osError_osScanFile] FOREIGN KEY([ScanFileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[osError] CHECK CONSTRAINT [FK_osError_osScanFile]
GO
ALTER TABLE [dbo].[osExcelProperty]  WITH CHECK ADD  CONSTRAINT [FK_osExcelProperty_osScanFile] FOREIGN KEY([ScanFileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[osExcelPropertyLinked]  WITH CHECK ADD  CONSTRAINT [FK_osExcelPropertyLinked_osScanFile] FOREIGN KEY([ScanFileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[osPowerPointProperty]  WITH CHECK ADD  CONSTRAINT [FK_osPowerPointProperty_osScanFile] FOREIGN KEY([ScanFileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[osScanFile]  WITH CHECK ADD  CONSTRAINT [FK_osScanFile_osFileFormat] FOREIGN KEY([FileFormatID])
REFERENCES [dbo].[osFileFormat] ([FileFormatID])
GO
ALTER TABLE [dbo].[osScanFile]  WITH NOCHECK ADD  CONSTRAINT [FK_osScanFile_osScan] FOREIGN KEY([ScanID])
REFERENCES [dbo].[osScan] ([ScanID])
GO
ALTER TABLE [dbo].[osScanFile]  WITH NOCHECK ADD  CONSTRAINT [FK_osScanFile_omCSIDL] FOREIGN KEY([CSIDL])
REFERENCES [dbo].[omCSIDL] ([CSIDL])
GO
ALTER TABLE [dbo].[osScanFile] CHECK CONSTRAINT [FK_osScanFile_osScan]
GO
ALTER TABLE [dbo].[osScanIncludedFolder]  WITH CHECK ADD  CONSTRAINT [FK_osScanIncludedFolder_osScan] FOREIGN KEY([ScanID])
REFERENCES [dbo].[osScan] ([ScanID])
GO
ALTER TABLE [dbo].[osScanExcludedFolder]  WITH CHECK ADD  CONSTRAINT [FK_osScanExcludedFolder_osScan] FOREIGN KEY([ScanID])
REFERENCES [dbo].[osScan] ([ScanID])
GO
ALTER TABLE [dbo].[osScanMappedDrive]  WITH CHECK ADD  CONSTRAINT [FK_osScanMappedDrive_osScan] FOREIGN KEY([ScanID])
REFERENCES [dbo].[osScan] ([ScanID])
GO
ALTER TABLE [dbo].[osScanSummary]  WITH CHECK ADD  CONSTRAINT [FK_osScanSummary_osScan] FOREIGN KEY([ScanID])
REFERENCES [dbo].[osScan] ([ScanID])
GO
ALTER TABLE [dbo].[osVBAProperty]  WITH CHECK ADD  CONSTRAINT [FK_osVBAProperty_osScanFile] FOREIGN KEY([ScanFileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO
ALTER TABLE [dbo].[osWordProperty]  WITH CHECK ADD  CONSTRAINT [FK_osWordProperty_osScanFile] FOREIGN KEY([ScanFileID])
REFERENCES [dbo].[osScanFile] ([ScanFileID])
GO


CREATE VIEW [dbo].[Uv_File]
AS
	SELECT 
		F.FileId, 
		F.Name,
		F.DNS AS Domain,
		F.ComputerName,
		F.Path,
		F.ShortPath,
		F.UserContext,
		FF.Description AS FileFormat,
		F.Size,
		F.ModifiedDate,
		MIL.Description AS MaxIssueLevel,
		F.IsReadOnly,
		F.CreatedDate,
		F.Owner
	FROM omFile F (NOLOCK) 
	INNER JOIN omIssueLevel MIL (NOLOCK) ON MIL.IssueLevelId = F.MaxIssueLevel 
	INNER JOIN osFileFormat FF (NOLOCK) ON FF.FileFormatID = F.FileFormatId 
GO

CREATE VIEW [dbo].[Uv_FileIssue]
AS
	SELECT 
		FI.FileId,
		IL.Description AS IssueLevel,
		IT.Description AS IssueType,
		I.Title,
		FI.IssueDate,
		I.Description,
		I.HelpURL
	FROM omFileIssue FI (NOLOCK) 
	INNER JOIN omIssue I (NOLOCK) ON I.IssueId = FI.IssueId 
	INNER JOIN omIssueLevel IL (NOLOCK) ON IL.IssueLevelId = I.IssueLevelId
	INNER JOIN omIssueType IT (NOLOCK) ON IT.IssueTypeId = I.IssueTypeId
	WHERE FI.IsResolved=0
GO

CREATE VIEW [dbo].[Uv_FileAction]
AS
	SELECT
		A.FileId,
		T.Title,
		T.Description,
		T.HelpURL,
		A.ActionDate,
		A.ActionOptions
	FROM omAction A (NOLOCK)
	INNER JOIN omTool T (NOLOCK) ON T.ToolId = A.ToolId
GO

CREATE VIEW [dbo].[Uv_FileCreatedFile]
AS
	SELECT
		AF.FileId,
		T.Title AS Tool,
		AF.ActionDate,
		FC.Description AS Type,
		AF.ComputerName, 
		AF.Path,
		AF.Name,
		AF.Domain
	FROM omActionFile AF (NOLOCK)
	INNER JOIN omTool T (NOLOCK) ON T.ToolId = AF.ToolId
	INNER JOIN omFileCategory FC (NOLOCK) ON FC.FileCategoryId = AF.FileCategoryId
GO

CREATE VIEW [dbo].[Uv_Issue]
AS
	SELECT DISTINCT
		I.IssueId,
		IL.IssueLevelId,
		IL.Description AS IssueLevel,
		IT.Description AS IssueType,
		I.Title,
		I.HelpURL,
		I.Description
	FROM omFileIssue FI (NOLOCK) 
	INNER JOIN omIssue I (NOLOCK) ON I.IssueId = FI.IssueId
	INNER JOIN omIssueLevel IL (NOLOCK) ON IL.IssueLevelId = I.IssueLevelId
	INNER JOIN omIssueType IT (NOLOCK) ON IT.IssueTypeId = I.IssueTypeId
GO

CREATE VIEW [dbo].[Uv_IssueLevel]
AS
	SELECT
		IssueLevelId,
		Description AS IssueLevel
	FROM omIssueLevel (NOLOCK)
GO

CREATE FUNCTION Fn_ScanErrors (@runID INT)
returns INT
AS
BEGIN
DECLARE @scanErrors INT
SELECT @scanErrors = SUM(CSE.CountScanErrors) 
FROM (SELECT COUNT(E.ErrorID) CountScanErrors 
        FROM osError E (NOLOCK) JOIN osScan S2 (NOLOCK)
        ON E.ScanID = S2.ScanId 
                WHERE S2.RunId = @runID) AS CSE

RETURN (@scanErrors)
END
GO

CREATE FUNCTION Fn_FilesScanned (@runID INT)
returns INT
AS
BEGIN
DECLARE @FilesScanned INT
SELECT @FilesScanned = SUM(CFN.CountScanFiles) 
                FROM (SELECT COUNT(F.FileName) CountScanFiles 
                        FROM osScanFile F (NOLOCK) JOIN osScan S2 (NOLOCK) 
                        ON F.ScanID = S2.ScanID 
                                WHERE S2.RunId = @runID) AS CFN 

RETURN (@FilesScanned)
END
GO

CREATE FUNCTION Fn_FileScanErrors (@runID INT)
returns INT
AS
BEGIN
DECLARE @FileScanErrors INT
SELECT @FileScanErrors = SUM(CFSE.CountFileScanErrors) 
                FROM (SELECT COUNT(E.ErrorID) CountFileScanErrors 
                        FROM osError E (NOLOCK) JOIN osScan S2 (NOLOCK) 
                        ON E.ScanID = S2.ScanID AND E.ScanFileID IS NOT NULL 
                                WHERE S2.RunId = @RunID) AS CFSE

RETURN (@FileScanErrors)
END
GO

CREATE VIEW [dbo].[Uv_Run]
AS
	SELECT DISTINCT
		S.RunId,
		S.Description AS RunDescription,
        dbo.Fn_ScanErrors(S.RunId) AS ScanErrors,
        dbo.Fn_FilesScanned(S.RunId) AS FilesScanned,
        dbo.Fn_FileScanErrors(S.RunId) AS FileScanErrors,
		S.AccessScan AS AccessDeepScan,
		S.ScanDAO AS ScanAccessDataObjects,
		S.MaxCopyFileSize,
		S.ScanMyDocuments,
		S.ScanDesktop,
		S.DeepScan
	FROM osScan S (NOLOCK) 
GO

CREATE VIEW [dbo].[Uv_RunComputer]
AS
	SELECT 
		S.RunId,
		S.ScanId,
		S.DNS AS Domain,
		S.ComputerName, 
		S.UserName,
		S.OS, 
		SS.StartDateTime,
		SS.EndDateTime,
		SS.Recoveries,
		COUNT(F.FileName) AS FilesScanned,
		(SELECT COUNT(*) FROM osError E (NOLOCK) WHERE E.ScanID = S.ScanID) AS ScannerErrors
	FROM osScan S (NOLOCK)
	INNER JOIN osScanFile F (NOLOCK) ON F.ScanId = S.ScanId
	LEFT JOIN osScanSummary SS (NOLOCK) ON SS.ScanId = S.ScanId
	GROUP BY
		S.RunId,
		S.ScanId,
		S.DNS,
		S.ComputerName,
		S.UserName,
		S.OS,
		SS.StartDateTime,
		SS.EndDateTime,
		SS.Recoveries
GO

CREATE VIEW [dbo].[Uv_RunError]
AS	
	SELECT DISTINCT
		S.RunId,
		S.ScanId,
		E.ErrorId,
		SF.FileName,
		SF.FilePath,
		ET.ErrorDescription AS Description,
		E.ErrorInfo
	FROM osScan S (NOLOCK)
	INNER JOIN osError E (NOLOCK) ON E.ScanId = S.ScanId 
	INNER JOIN osErrorText ET (NOLOCK) ON ET.ErrorId = E.ErrorId
	LEFT JOIN osScanFile SF (NOLOCK) ON SF.ScanID = S.ScanId AND E.ScanFileId = SF.ScanFileId
	GROUP BY 
		S.RunId,
		S.ScanId,
		E.ErrorId,
		SF.FileName,
		SF.FilePath,
		ET.ErrorDescription,
		E.ErrorInfo
GO

/****** Object:  View [dbo].[Uv_ApplyFilterFile]    Script Date: 07/06/2006 08:09:22 ******/
CREATE VIEW [dbo].[Uv_ApplyFilterFile]
AS
	SELECT S.RunID, 
		F.FileId, 
		MIL.IssueLevelId AS MaxIssueLevelId, 
		MIL.Description AS MaxIssueLevel, 
		IT.IssueTypeId, 
		I.IssueId, 
		F.Size, 
		F.ModifiedDate, 
		F.IsReadOnly, 
		F.FileFormatId, 
		FF.Description AS FileFormat, 
		F.Extension, 
		F.Name, 
		F.DNS, 
		F.Path, 
		F.ComputerName, 
		F.UserContext, 
		F.CSIDL, 
		C.Name AS CSIDLName,
		FI.IsResolved
	FROM omFile F (NOLOCK) 
	INNER JOIN omIssueLevel MIL (NOLOCK) ON MIL.IssueLevelId = F.MaxIssueLevel 
	INNER JOIN osFileFormat FF (NOLOCK) ON FF.FileFormatID = F.FileFormatId 
	INNER JOIN omFileScanFile FSF (NOLOCK) ON FSF.FileId = F.FileId 
	INNER JOIN osScanFile SF (NOLOCK) ON SF.ScanFileID = FSF.ScanFileId 
	INNER JOIN omCSIDL C (NOLOCK) ON C.CSIDL = F.CSIDL 
	INNER JOIN osScan S (NOLOCK) ON S.ScanID = SF.ScanID 
	LEFT OUTER JOIN omFileIssue FI (NOLOCK) ON FI.FileId = F.FileId 
	LEFT OUTER JOIN omIssue I (NOLOCK) ON I.IssueId = FI.IssueId 
	LEFT OUTER JOIN omIssueType IT (NOLOCK) ON IT.IssueTypeId = I.IssueTypeId
GO

/****** Object:  View [dbo].[Uv_Filter]    Script Date: 07/17/2006 12:13:32 ******/
CREATE VIEW [dbo].[Uv_Filter]
AS
	SELECT DISTINCT 
		FilterId, 
		Name,
		Advanced,
		SQLText
	FROM omFilter (NOLOCK) 
	WHERE FilterId > 0
GO

/****** Object:  View [dbo].[Uv_FilterFileAction]    Script Date: 07/06/2006 08:09:22 ******/
CREATE VIEW [dbo].[Uv_FilterFileAction]
AS
	SELECT DISTINCT 
		T.ToolId, 
		T.Title AS ToolName, 
		A.ActionOptions
	FROM omAction A (NOLOCK)
	INNER JOIN omTool T (NOLOCK) ON T.ToolId = A.ToolId
GO

/****** Object:  View [dbo].[Uv_FilterFileIssue]    Script Date: 07/06/2006 08:09:22 ******/
CREATE VIEW [dbo].[Uv_FilterFileIssue]
AS
	SELECT DISTINCT 
		I.IssueId, 
		I.Title AS IssueTitle, 
		IL.Description AS IssueLevel, 
		IL.IssueLevelId, 
		IT.IssueTypeId
	FROM omFileIssue FI (NOLOCK) 
	INNER JOIN omIssue I (NOLOCK) ON I.IssueId = FI.IssueId 
	INNER JOIN omIssueLevel IL (NOLOCK) ON IL.IssueLevelId = I.IssueLevelId 
	INNER JOIN omIssueType IT (NOLOCK) ON IT.IssueTypeId = I.IssueTypeId
	WHERE FI.IsResolved = 0
UNION
	SELECT NULL AS IssueId, 
		'(Clear Filter)' AS IssueTitle, 
		NULL AS IssueLevel, 
		NULL AS IssueLevelId, 
		NULL AS IssueTypeId

GO

/****** Object:  View [dbo].[Uv_FilterFileIssueResolved]    Script Date: 07/17/2006 10:56:34 ******/
CREATE VIEW [dbo].[Uv_FilterFileIssueResolved]
AS
	SELECT DISTINCT 
		I.IssueId, 
		I.Title AS IssueTitle, 
		IL.IssueLevelId, 
		IT.IssueTypeId
	FROM omFileIssue FI (NOLOCK) 
	INNER JOIN omIssue I (NOLOCK) ON I.IssueId = FI.IssueId 
	INNER JOIN omIssueLevel IL (NOLOCK) ON IL.IssueLevelId = I.IssueLevelId 
	INNER JOIN omIssueType IT (NOLOCK) ON IT.IssueTypeId = I.IssueTypeId
	WHERE FI.IsResolved = 1
UNION
	SELECT NULL AS IssueId, 
		'(Clear Filter)' AS IssueTitle, 
		NULL AS IssueLevelId, 
		NULL AS IssueTypeId
GO

/****** Object:  View [dbo].[Uv_FilterFileIssueLevel]    Script Date: 07/06/2006 08:09:22 ******/
CREATE VIEW [dbo].[Uv_FilterFileIssueLevel]
AS
	SELECT DISTINCT 
	    ISNULL(IL.IssueLevelId, 4) AS IssueLevelId, 
	    ISNULL(IL.Description, 'No Issue') AS IssueLevel
	FROM omFile AS F WITH (NOLOCK)
        LEFT JOIN omFileIssue AS FI WITH (NOLOCK) ON FI.FileId = F.FileId
        LEFT JOIN omIssue AS I WITH (NOLOCK) ON I.IssueId = FI.IssueId
        LEFT JOIN omIssueLevel AS IL WITH (NOLOCK) ON IL.IssueLevelId = I.IssueLevelId
UNION
	SELECT NULL AS IssueLevelId, 
		'(Clear Filter)' AS IssueLevel

GO

/****** Object:  View [dbo].[Uv_FilterFileIssueType]    Script Date: 07/06/2006 08:09:22 ******/
CREATE VIEW [dbo].[Uv_FilterFileIssueType]
AS
	SELECT DISTINCT 
		IT.IssueTypeId, 
		IT.Description AS IssueType
	FROM omFileIssue FI (NOLOCK) 
	INNER JOIN omIssue I (NOLOCK) ON I.IssueId = FI.IssueId 
	INNER JOIN omIssueType IT (NOLOCK) ON IT.IssueTypeId = I.IssueTypeId
UNION
	SELECT NULL AS IssueTypeId, 
		'(Clear Filter)' AS IssueType
GO

/****** Object:  View [dbo].[Uv_FilterFileFormat]    Script Date: 07/06/2006 08:09:22 ******/
CREATE VIEW [dbo].[Uv_FilterFileFormat]
AS
	SELECT DISTINCT 
		FF.FileFormatID, 
		FF.Description AS FileFormat
	FROM omFile F (NOLOCK) 
	INNER JOIN osFileFormat FF (NOLOCK) ON FF.FileFormatID = F.FileFormatId
UNION
	SELECT NULL AS FileFormatID, 
		'(Clear Filter)' AS FileFormat
UNION 
	SELECT -1 AS FileFormatID,
		'Excel / PowerPoint / Word' AS FileFormat
GO

/****** Object:  View [dbo].[Uv_FilterFileExtension]    Script Date: 07/06/2006 08:09:22 ******/
CREATE VIEW [dbo].[Uv_FilterFileExtension]
AS
	SELECT DISTINCT 
		FF.Description AS FileFormat, 
		F.Extension
	FROM omFile F (NOLOCK) 
	INNER JOIN osFileFormat FF (NOLOCK) ON FF.FileFormatID = F.FileFormatId
UNION
	SELECT NULL AS FileFormat, 
		'(Clear Filter)' AS Extension
GO

/****** Object:  View [dbo].[Uv_FilterFileDomain]    Script Date: 07/06/2006 08:09:22 ******/
CREATE VIEW [dbo].[Uv_FilterFileDomain]
AS
	SELECT DISTINCT 
		DNS AS Domain
	FROM omFile F (NOLOCK)
UNION
	SELECT '(Clear Filter)' AS Domain
GO

/****** Object:  View [dbo].[Uv_FilterFileCSIDL]    Script Date: 07/06/2006 08:09:22 ******/
CREATE VIEW [dbo].[Uv_FilterFileCSIDL]
AS
	SELECT DISTINCT 
		F.CSIDL, 
		C.Name
	FROM omFile F (NOLOCK) 
	INNER JOIN omCSIDL C (NOLOCK) ON C.CSIDL = F.CSIDL
UNION
	SELECT NULL AS CSIDL, 
		'(Clear Filter)' AS Name
GO

/****** Object:  View [dbo].[Uv_FilterFileRunId]    Script Date: 07/17/2006 10:59:20 ******/
CREATE VIEW [dbo].[Uv_FilterFileRunId]
AS
	SELECT DISTINCT 
		RunID, 
		Description
	FROM osScan S (NOLOCK)
UNION
	SELECT NULL AS RunId, 
		'(Clear Filter)' AS Description
GO

/****** Object:  StoredProcedure [dbo].[Xp_ExportFileList]    Script Date: 06/09/2006 10:56:51 ******/
CREATE PROCEDURE [dbo].[Xp_ExportFileList] ( 
    @Domain NVARCHAR(256), 
    @ComputerName NVARCHAR(48), 
    @LastFileId INT,
    @FilterId INT = NULL) 
AS 

DECLARE @ERROR_MSG              VARCHAR (255),
            @SQLParms           NVARCHAR(512),
            @SQLString          NVARCHAR(4000),
            @SQLText            NVARCHAR(3600),
            @Count              INT

SET @SQLText = ''


-- Get the filter criteria 
IF ISNULL(@FilterId, -1) >= 0
BEGIN

    SELECT @SQLText = SQLText FROM omFilter WHERE FilterId = @FilterId

    IF @SQLText IS NULL 
    BEGIN
        SET @ERROR_MSG = 'ERROR: Unable To Export File List, Specified Filter ID Does Not Exist.'
        GOTO EXIT_ERROR
    END
END

If @SQLText LIKE 'WHERE%'
BEGIN
	SET @SQLText = @SQLText + ' AND FileId > @LastFileId'
END

If @SQLText = '' 
BEGIN
	SET @SQLText = 'WHERE FileId > @LastFileId'
END

-- Generate the export xml
SET @SQLParms = '@Domain NVARCHAR(256), @ComputerName NVARCHAR(48), @LastFileId INT'
SET @SQLString = 'SELECT DISTINCT  '
SET @SQLString = @SQLString + 'Files.FileId, '
SET @SQLString = @SQLString + 'Files.DNS, '
SET @SQLString = @SQLString + 'Files.ComputerName, '
SET @SQLString = @SQLString + 'Files.Path, '
SET @SQLString = @SQLString + 'Files.Name, '
SET @SQLString = @SQLString + 'Files.FileFormatId, '
SET @SQLString = @SQLString + 'Files.ModifiedDate, '
SET @SQLString = @SQLString + 'Files.UserContext, '
SET @SQLString = @SQLString + 'Issues.IssueId '
SET @SQLString = @SQLString + 'FROM omFile Files (NOLOCK) '
SET @SQLString = @SQLString + 'INNER JOIN (SELECT DISTINCT TOP 1000 FileId FROM Uv_ApplyFilterFile ' + @SQLText + ' ORDER BY FileId) X ON X.FileId = Files.FileId '
SET @SQLString = @SQLString + 'LEFT JOIN (SELECT * FROM omFileIssue Issues (NOLOCK) WHERE Issues.IsResolved = 0) Issues ON Issues.FileId = Files.FileId '
SET @SQLString = @SQLString + 'WHERE Files.DNS = @Domain '
SET @SQLString = @SQLString + 'AND Files.ComputerName = @ComputerName '
SET @SQLString = @SQLString + 'ORDER BY Files.FileId ASC '
SET @SQLString = @SQLString + 'FOR XML AUTO, ELEMENTS '

EXEC SP_EXECUTESQL @SQLString, @SQLParms, @Domain, @ComputerName, @LastFileId

IF @@ERROR <> 0
BEGIN
    SET @ERROR_MSG = 'ERROR: Unable To Export File List'
    GOTO EXIT_ERROR
END

EXIT_PROC:
    SET NOCOUNT OFF
    RETURN 0

EXIT_ERROR:
    SET NOCOUNT OFF
    RAISERROR(@ERROR_MSG, 16, 1)
    RETURN -1
GO

/****** Object:  StoredProcedure [dbo].[Xp_ImportToolDef]    Script Date: 06/09/2006 10:56:51 ******/
CREATE PROCEDURE [dbo].[Xp_ImportToolDef] @tool_def_xml ntext 
AS 
BEGIN 
DECLARE @doc_handle int; 
EXEC sp_xml_preparedocument @doc_handle OUTPUT, @tool_def_xml; 

SET XACT_ABORT ON

Begin tran
INSERT [dbo].[omTool] 
SELECT * 
FROM OPENXML (@doc_handle, N'/OMPMTools/Tool', 2) 
WITH [dbo].[omTool] 
WHERE ToolId NOT IN (Select ToolId From omTool) 

INSERT [dbo].[omIssue] 
SELECT * 
FROM OPENXML (@doc_handle, N'/OMPMTools/Tool/Issues/Issue', 2) 
WITH [dbo].[omIssue] 
WHERE IssueId NOT IN (Select IssueId FROM omIssue) 

INSERT [dbo].[omToolIssue] 
SELECT ToolId, IssueId 
FROM OPENXML (@doc_handle, N'/OMPMTools/Tool/Issues/Issue', 2)
WITH (ToolId	int		'../../ToolId',       IssueId  int 'IssueId') AS NewTool 
WHERE NOT EXISTS (Select Tool.ToolId, Tool.IssueId From [dbo].[omToolIssue] AS Tool        
	WHERE Tool.ToolId = NewTool.ToolId AND Tool.IssueId = NewTool.IssueId) 
	
INSERT [dbo].[omFileCategory] 
SELECT * 
FROM OPENXML (@doc_handle, N'/OMPMTools/Tool/OutputFileCategories/OutputFileCategory', 2) 
WITH [dbo].[omFileCategory] 
WHERE FileCategoryId NOT IN (Select FileCategoryId FROM omFileCategory) 

Commit tran

EXEC sp_xml_removedocument @doc_handle; 
END 
GO

/****** Object:  StoredProcedure [dbo].[Xp_UpdateMaxIssueLevel]    Script Date: 06/09/2006 10:56:51 ******/
CREATE PROCEDURE [dbo].[Xp_UpdateMaxIssueLevel]
AS

SET NOCOUNT ON

-- Calculate and update the max issue level for all files
UPDATE  omFile
SET     MaxIssueLevel = ISNULL(XFI.IssueLevelId, 4)
FROM    omFile F
        LEFT JOIN (SELECT  FI.FileId, MIN(I.IssueLevelId) AS IssueLevelId
                    FROM    omFileIssue FI
                            INNER JOIN omIssue I ON I.IssueId = FI.IssueId
                    WHERE FI.IsResolved = 0
                    GROUP BY Fi.FileId) XFI
             ON XFI.FileId = F.FileId

GO

/****** Object:  StoredProcedure [dbo].[Xp_PostScanIssuesData]    Script Date: 06/09/2006 10:56:51 ******/
CREATE PROCEDURE [dbo].[Xp_PostScanIssuesData] (
    @RunId          INT,
    @IssueId        INT,
    @SQLTable       NVARCHAR (128),
    @SQLFilter      NVARCHAR (512)
)
AS

SET NOCOUNT ON

DECLARE @ERROR_MSG      VARCHAR (255),
        @SQLParms       NVARCHAR(512),
        @SQLString      NVARCHAR(1024),
		@CurrentDate	DATETIME
		
SET @CurrentDate = GETUTCDATE()

SET @SQLParms = '@SQLRunId INT, @SQLIssueId INT, @CurrentDate DATETIME'
SET @SQLString = 'INSERT INTO omFileIssue '
SET @SQLString = @SQLString + 'SELECT FileId = F.FileId, '
SET @SQLString = @SQLString + 'IssueId = @SQLIssueId, '
SET @SQLString = @SQLString + 'IssueDate = @CurrentDate, '
SET @SQLString = @SQLString + 'IsResolved = 0 '
SET @SQLString = @SQLString + 'FROM omFile F '
SET @SQLString = @SQLString + 'INNER JOIN omFileScanFile FSF ON FSF.FileId = F.FileId '
SET @SQLString = @SQLString + 'INNER JOIN osScanFile SF ON SF.ScanFileId = FSF.ScanFileId '
SET @SQLString = @SQLString + 'INNER JOIN osScan S ON S.ScanId = SF.ScanId '
SET @SQLString = @SQLString + 'INNER JOIN ' + @SQLTable + ' P ON P.ScanFileId = SF.ScanFileId '
SET @SQLString = @SQLString + 'LEFT JOIN  omFileIssue FI ON FI.FileId = F.FileId '
SET @SQLString = @SQLString + 'AND FI.IssueId = @SQLIssueId '
SET @SQLString = @SQLString + 'WHERE FI.FileId IS NULL '
SET @SQLString = @SQLString + 'AND S.RunId = @SQLRunId '
SET @SQLString = @SQLString + 'AND ' + @SQLFilter

EXEC SP_EXECUTESQL @SQLString, @SQLParms, @RunId, @IssueId, @CurrentDate
GO

/****** Object:  StoredProcedure [dbo].[Xp_PostScanIssues]    Script Date: 06/09/2006 10:56:51 ******/
CREATE PROCEDURE [dbo].[Xp_PostScanIssues] (
    @RunId    INT
)
AS

SET NOCOUNT ON

DECLARE @ERROR_MSG      VARCHAR (255)


-- Generate WORD Issues
EXEC Xp_PostScanIssuesData @RunId, 1100, N'osWordProperty', N'HaveVersions = 1'


-- Generate POWERPOINT Issues
EXEC Xp_PostScanIssuesData @RunId, 1200, N'osPowerPointProperty', N'P.hasSendForReviewData = 1'
EXEC Xp_PostScanIssuesData @RunId, 1201, N'osPowerPointProperty', N'P.hasEmbeddings = 1'
EXEC Xp_PostScanIssuesData @RunId, 1202, N'osPowerPointProperty', N'P.hasVBA = 1'
EXEC Xp_PostScanIssuesData @RunId, 1203, N'osPowerPointProperty', N'P.hasMicrosoftScriptEditorData = 1'
EXEC Xp_PostScanIssuesData @RunId, 1204, N'osPowerPointProperty', N'P.hasPresentationBroadcastData = 1'
EXEC Xp_PostScanIssuesData @RunId, 1205, N'osPowerPointProperty', N'P.hasDocumentRoutingSlip = 1'
EXEC Xp_PostScanIssuesData @RunId, 1206, N'osPowerPointProperty', N'P.hasPublishandSubscribeData = 1'
EXEC Xp_PostScanIssuesData @RunId, 1207, N'osPowerPointProperty', N'P.hasLargeNumberofOLEObjects = 1'


-- Generate EXCEL Issues
EXEC Xp_PostScanIssuesData @RunId, 1300, N'osExcelProperty', N'P.FileOpenNotSupported = 1'
EXEC Xp_PostScanIssuesData @RunId, 1301, N'osExcelProperty', N'P.FileSaveNotSupported = 1'
EXEC Xp_PostScanIssuesData @RunId, 1302, N'osExcelProperty', N'P.HTMLSaved = 1'
EXEC Xp_PostScanIssuesData @RunId, 1303, N'osExcelProperty', N'P.WorkspaceFile = 1'
EXEC Xp_PostScanIssuesData @RunId, 1304, N'osExcelProperty', N'P.FileFormat = ''BIFF5'''
EXEC Xp_PostScanIssuesData @RunId, 1305, N'osExcelProperty', N'(NULLIF(P.WSSLinkedList, '''') IS NOT NULL AND P.WSSLinkedList <> ''0'')'
EXEC Xp_PostScanIssuesData @RunId, 1306, N'osExcelProperty', N'P.MSERedcords = 1'
EXEC Xp_PostScanIssuesData @RunId, 1307, N'osExcelProperty', N'EXISTS (SELECT ScanFileId FROM osExcelPropertyLinked WHERE ScanFileId = SF.ScanFileId)'
EXEC Xp_PostScanIssuesData @RunId, 1308, N'osExcelProperty', N'ISNULL(P.Charts, 0) > 0'
EXEC Xp_PostScanIssuesData @RunId, 1309, N'osExcelProperty', N'P.ELFEnabled = 1'
EXEC Xp_PostScanIssuesData @RunId, 1310, N'osExcelProperty', N'(P.EmbeddedDocs <> ''0'' AND P.EmbeddedDocs IS NOT NULL)'
EXEC Xp_PostScanIssuesData @RunId, 1311, N'osExcelProperty', N'P.OWC9 = 1'
EXEC Xp_PostScanIssuesData @RunId, 1312, N'osExcelProperty', N'P.OWC10 = 1'
EXEC Xp_PostScanIssuesData @RunId, 1313, N'osExcelProperty', N'P.OWC11 = 1'

GO

/****** Object:  StoredProcedure [dbo].[Xp_PostScanFiles]    Script Date: 06/09/2006 10:56:51 ******/
Create PROCEDURE [dbo].[Xp_PostScanFiles]
AS

SET NOCOUNT ON

DECLARE @RunId          INT,		
		@CurrentDate	DATETIME
		
SET @CurrentDate = GETUTCDATE()

-- Get the earliest RunId that has unprocessed files
SELECT  @RunId = MIN(S.RunId)
FROM    osScan S 
        INNER JOIN osScanFile SF ON SF.ScanId = S.ScanId
        LEFT JOIN omFileScanFile FSF ON FSF.ScanFileId = SF.ScanFileId
WHERE   FSF.ScanFileId IS NULL


-- Process files for each RunId found
WHILE ISNULL(@RunId, 0) > 0
BEGIN

    -- Insert a relationship for existing files
    INSERT INTO omFileScanFile
    SELECT  F.FileId,
            FSF.ScanFileId
    FROM    (SELECT s.ScanFileId, s.FileName, s.FilePath, s.ScanId, s.HashCode
                        FROM   osScanFile s (NOLOCK)
                        LEFT JOIN omFileScanFile o (NOLOCK)
                            ON s.ScanFileId = o.ScanFileId
                        WHERE o.ScanFileId IS NULL) FSF
            INNER JOIN osScan S (NOLOCK) 
                 ON S.ScanId = FSF.ScanId
            INNER JOIN omFile F (NOLOCK) 
                 ON F.Name          = FSF.FileName
                AND F.Path          = FSF.FilePath
                AND F.ComputerName  = S.ComputerName
                AND F.UserContext   = S.UserName
                AND F.DNS           = S.DNS
                AND F.HashCode      = FSF.HashCode
    WHERE   S.RunId = @RunId


    -- Delete issues for files that have been modified since the last scan
    DELETE  FROM omFileIssue
    FROM    omFileIssue FI
            INNER JOIN omFile F 
                ON F.FileId = FI.FileId
            INNER JOIN omFileScanFile FSF 
                ON FSF.FileId = FI.FileId
            INNER JOIN osScanFile SF 
                ON SF.ScanFileId = FSF.ScanFileId
            INNER JOIN osScan S 
                ON S.ScanId = SF.ScanId
    WHERE   SF.ModifiedDate > F.ModifiedDate
      AND   S.RunId         = @RunId


    -- Update the file data for existing files
    UPDATE  omFile
       SET  LastScanFileId  = SF.ScanFileId,
			Size            = SF.FileSize,
            CreatedDate     = SF.CreatedDate,
            ModifiedDate    = SF.ModifiedDate,
            Owner           = SF.FileOwner
    FROM    osScanFile SF
            INNER JOIN osScan S 
                ON S.ScanId = SF.ScanId
            INNER JOIN omFileScanFile FSF 
                ON FSF.ScanFileId = SF.ScanFileId
            INNER JOIN omFile F 
                ON F.FileId = FSF.FileId
    WHERE   S.RunId = @RunId
      AND   (   F.Size         <> SF.FileSize 
             OR F.CreatedDate  <> SF.CreatedDate 
             OR F.ModifiedDate <> SF.ModifiedDate 
             OR F.Owner        <> SF.FileOwner)


    -- Insert new files found
    INSERT INTO omFile
    SELECT  SF.ScanFileId,
			SF.FileName,
            SF.FilePath,
            SF.ShortFilePath,
            SF.FileExtension,
            SF.FileFormatId,
            SF.FileSize,
            SF.CreatedDate,
            SF.ModifiedDate,
            SF.FileOwner,
            S.UserName,
            S.ComputerName,
            S.DNS,
            SF.HashCode,
            SF.CSIDL,
            3,
            SF.IsReadOnly
    FROM    osScanFile SF
            INNER JOIN osScan S 
                ON S.ScanId = SF.ScanId
            LEFT JOIN omFileScanFile FSF 
                ON FSF.ScanFileId = SF.ScanFileId
    WHERE   FSF.ScanFileId IS NULL
      AND   S.RunId = @RunId


    -- Insert a relationship for the new files
    INSERT INTO omFileScanFile
    SELECT  F.FileId,
            FSF.ScanFileId
    FROM    (SELECT s.ScanFileId, s.FileName, s.FilePath, s.ScanId, s.HashCode
                        FROM   osScanFile s (NOLOCK)
                        LEFT JOIN omFileScanFile o (NOLOCK)
                            ON s.ScanFileId = o.ScanFileId
                        WHERE o.ScanFileId IS NULL) FSF
            INNER JOIN osScan S (NOLOCK) 
                 ON S.ScanId = FSF.ScanId
            INNER JOIN omFile F (NOLOCK) 
                 ON F.Name          = FSF.FileName
                AND F.Path          = FSF.FilePath
                AND F.ComputerName  = S.ComputerName
                AND F.UserContext   = S.UserName
                AND F.DNS           = S.DNS
                AND F.HashCode      = FSF.HashCode
    WHERE   S.RunId = @RunId


    -- Insert an issue for files not deep scanned
    INSERT INTO omFileIssue
    SELECT  FSF.FileId,
            1010,
            @CurrentDate,
            0
    FROM    omFileScanFile FSF
            INNER JOIN osScanFile SF
                ON SF.ScanFileId = FSF.ScanFileId
            INNER JOIN osScan S 
                ON S.ScanId = SF.ScanId
            LEFT JOIN omFileIssue FI
                ON FI.FileId = FSF.FileId
    WHERE   FI.FileId   IS NULL
      AND   S.RunId     = @RunId
      AND   S.DeepScan  = 0


    -- Insert an issue for files with scan errors
    INSERT INTO omFileIssue
    SELECT  FSF.FileId,
            1050,
            @CurrentDate,
            0
    FROM    omFileScanFile FSF
            INNER JOIN (SELECT DISTINCT ScanFileId 
                        FROM osError (NOLOCK)) E
                ON E.ScanFileId = FSF.ScanFileId
            INNER JOIN osScanFile SF
                ON SF.ScanFileId = FSF.ScanFileId
            INNER JOIN osScan S 
                ON S.ScanId = SF.ScanId
            LEFT JOIN omFileIssue FI
                ON FI.FileId = FSF.FileId
    WHERE   FI.FileId   IS NULL
      AND   S.RunId     = @RunId


    -- Generate product specific issues
    EXEC Xp_PostScanIssues @RunId


    -- Get the next RunId that has unprocessed files
    SELECT  @RunId = MIN(S.RunId)
    FROM    osScan S 
            INNER JOIN osScanFile SF ON SF.ScanId = S.ScanId
            LEFT JOIN omFileScanFile FSF ON FSF.ScanFileId = SF.ScanFileId
    WHERE   FSF.ScanFileId IS NULL
      AND   RunId > @RunId

END


-- Update the Issue Level for all files
EXEC Xp_UpdateMaxIssueLevel

SET NOCOUNT OFF
RETURN 0

GO

GO

/****** Object:  StoredProcedure [dbo].[Xp_PostToolActions]    Script Date: 06/09/2006 10:56:51 ******/
CREATE PROCEDURE [dbo].[Xp_PostToolActions]
AS

    SET NOCOUNT ON

    DECLARE @ERROR_MSG      VARCHAR (255),
            @CurrentDate    DATETIME

    SET @CurrentDate = GETUTCDATE()


    BEGIN TRANSACTION

        -- Identify a working set of issues that need to be posted 
        -- against the omFileIssue Data
        UPDATE  omActionIssue
           SET  PostStatus      = 1,
                PostDate        = @CurrentDate
        WHERE   PostStatus      IS NULL
           OR   PostStatus      = 0

        IF @@ERROR <> 0
        BEGIN
            SET @ERROR_MSG = 'ERROR: Unable to identify a working set of issues'
            GOTO EXIT_ROLLBACK
        END


        -- Resolve existing issues
        UPDATE  omFileIssue
           SET  IsResolved      = AI.IsResolved
        FROM    omFileIssue FI
                INNER JOIN omActionIssue AI
                    ON AI.FileId    = FI.FileId
                   AND AI.IssueId   = FI.IssueId
        WHERE   FI.IsResolved   = 0
          AND   AI.IsResolved   = 1
          AND   AI.PostStatus   = 1
          AND   AI.PostDate     = @CurrentDate

        IF @@ERROR <> 0
        BEGIN
            SET @ERROR_MSG = 'ERROR: Unable to resolve existing issues'
            GOTO EXIT_ROLLBACK
        END


        -- Create new issues
        INSERT INTO omFileIssue
        SELECT  FileId          = AI.FileId,
                IssueId         = AI.IssueId,
                IssueDate       = AI.ActionDate,
                IsResolved      = AI.IsResolved
        FROM    omActionIssue AI
                LEFT JOIN omFileIssue FI
                    ON FI.FileId    = AI.FileId
                   AND FI.IssueId   = AI.IssueId
        WHERE   FI.FileId       IS NULL
          AND   AI.PostStatus   = 1
          AND   AI.PostDate     = @CurrentDate

        IF @@ERROR <> 0
        BEGIN
            SET @ERROR_MSG = 'ERROR: Unable to create new issues'
            GOTO EXIT_ROLLBACK
        END


        -- Mark the working set of actions complete
        UPDATE  omActionIssue
           SET  PostStatus      = 2
        WHERE   PostStatus      = 1
           AND  PostDate        = @CurrentDate

        IF @@ERROR <> 0
        BEGIN
            SET @ERROR_MSG = 'ERROR: Unable to mark the working set of issues complete'
            GOTO EXIT_ROLLBACK
        END

    COMMIT TRANSACTION

-- Update the Issue Level for all files
EXEC Xp_UpdateMaxIssueLevel

EXIT_PROC:
    SET NOCOUNT OFF
    RETURN 0

EXIT_ROLLBACK:
    ROLLBACK TRANSACTION

EXIT_ERROR:
    SET NOCOUNT OFF
    RAISERROR(@ERROR_MSG, 16, 1)
    RETURN -1
GO

/****** Object:  StoredProcedure [dbo].[Up_FilterAdd]    Script Date: 06/09/2006 10:56:51 ******/
CREATE PROCEDURE [dbo].[Up_FilterAdd] (
    @Name       NVARCHAR(48),
    @SQLText    NVARCHAR(3600),
    @Advanced   BIT,
	@FilterId	INT = NULL
)
AS
    SET NOCOUNT ON

    DECLARE @ERROR_MSG      VARCHAR (255),
			@COUNT_ID		INT

	IF @FilterId IS NULL
	BEGIN
		INSERT INTO omFilter
		SELECT Name     = @Name,
			   SQLText  = @SQLText,
			   Advanced = @Advanced
	END

	IF @FilterId IS NOT NULL
	BEGIN
		SELECT @COUNT_ID = COUNT(*) FROM omFilter WHERE FilterId = @FilterId

		IF @COUNT_ID = 0
		BEGIN
			SET IDENTITY_INSERT omFilter ON
			INSERT INTO omFilter (FilterId, Name, SQLText, Advanced) 
				VALUES (@FilterId, @Name, @SQLText, @Advanced)
		END
		
		IF @COUNT_ID = 1
		BEGIN
			UPDATE omFilter
			SET Name    = @Name,
                SQLText  = @SQLText,
                Advanced = @Advanced
			WHERE  FilterId = @FilterId
		END
	END
	
	

    IF @@ERROR <> 0
    BEGIN
        SET @ERROR_MSG = 'ERROR: Unable to insert filter'
        GOTO EXIT_ERROR
    END


EXIT_PROC:
    SET NOCOUNT OFF
    RETURN 0

EXIT_ERROR:
    SET NOCOUNT OFF
    RAISERROR(@ERROR_MSG, 16, 1)
    RETURN -1
GO

/****** Object:  StoredProcedure [dbo].[Up_FilterUpdate]    Script Date: 06/09/2006 10:56:51 ******/
CREATE PROCEDURE [dbo].[Up_FilterUpdate] (
    @FilterId   INT,
    @Name       NVARCHAR(48),
    @SQLText    NVARCHAR(3600),
    @Advanced   BIT
)
AS

    SET NOCOUNT ON

    DECLARE @ERROR_MSG      VARCHAR (255)

    IF EXISTS (SELECT * FROM omFilter WHERE FilterId = @FilterId)
    BEGIN

        UPDATE omFilter
        SET    Name     = @Name,
               SQLText  = @SQLText,
               Advanced = @Advanced
        WHERE  FilterId = @FilterId

        IF @@ERROR <> 0
        BEGIN
            SET @ERROR_MSG = 'ERROR: Unable to update filter'
            GOTO EXIT_ERROR
        END

    END
    ELSE
    BEGIN

        SET @ERROR_MSG = 'ERROR: Filter not found'
        GOTO EXIT_ERROR

    END

EXIT_PROC:
    SET NOCOUNT OFF
    RETURN 0

EXIT_ERROR:
    SET NOCOUNT OFF
    RAISERROR(@ERROR_MSG, 16, 1)
    RETURN -1
GO

/****** Object:  StoredProcedure [dbo].[Up_FilterDelete]    Script Date: 06/09/2006 10:56:51 ******/
CREATE PROCEDURE [dbo].[Up_FilterDelete] (
    @FilterId   INT
)
AS

    SET NOCOUNT ON

    DECLARE @ERROR_MSG      VARCHAR (255)

    DELETE omFilter
    WHERE  FilterId = @FilterId

    IF @@ERROR <> 0
    BEGIN
        SET @ERROR_MSG = 'ERROR: Unable to delete filter'
        GOTO EXIT_ERROR
    END


EXIT_PROC:
    SET NOCOUNT OFF
    RETURN 0

EXIT_ERROR:
    SET NOCOUNT OFF
    RAISERROR(@ERROR_MSG, 16, 1)
    RETURN -1
GO

/****** Object:  StoredProcedure [dbo].[Up_UpdateIssueLevel]    Script Date: 07/24/2006 17:09:20 ******/
CREATE PROCEDURE [dbo].[Up_UpdateIssueLevel] (
	@IssueId		INT,
	@NewLevelId		INT
)
AS

SET NOCOUNT ON

DECLARE @ERROR_MSG      VARCHAR (255)


-- Update the issueid 
UPDATE	omIssue
SET		IssueLevelId = @NewLevelId
WHERE	IssueId = @IssueId

IF @@ERROR <> 0
BEGIN
	SET @ERROR_MSG = 'ERROR: Unable to update the issue level'
	GOTO EXIT_ERROR
END

EXEC Xp_UpdateMaxIssueLevel


EXIT_PROC:
    SET NOCOUNT OFF
    RETURN 0

EXIT_ERROR:
    SET NOCOUNT OFF
    RAISERROR(@ERROR_MSG, 16, 1)
    RETURN -1
GO

/****** Object:  StoredProcedure [dbo].[Up_FilterApplyFile]    Script Date: 07/06/2006 08:56:20 ******/
CREATE PROCEDURE [dbo].[Up_FilterApplyFile] (
    @SQLText    NVARCHAR(3600),
    @Records    INT = 1000
)
AS

    SET NOCOUNT ON

	DECLARE @ERROR_MSG      VARCHAR (255),
			@SQLParms       NVARCHAR(512),
			@SQLString      NVARCHAR(4000)

	SET @Records = ISNULL(@Records, 1000)

	SET @SQLParms = ''
	SET @SQLString = 'SELECT DISTINCT '
	
	IF @Records > 0
	BEGIN
		SET @SQLString = @SQLString + 'TOP '+ CONVERT(NVARCHAR(16), @Records) +' '
	END

	SET @SQLString = @SQLString + 'FileId, '
	SET @SQLString = @SQLString + 'MaxIssueLevel, '
	SET @SQLString = @SQLString + 'FileFormat, '
	SET @SQLString = @SQLString + 'Name, '
	SET @SQLString = @SQLString + 'ComputerName, '
	SET @SQLString = @SQLString + 'DNS, '
	SET @SQLString = @SQLString + 'UserContext, '
	SET @SQLString = @SQLString + 'Path, '
	SET @SQLString = @SQLString + 'ModifiedDate, '
	SET @SQLString = @SQLString + 'IsReadOnly, '
	SET @SQLString = @SQLString + 'CSIDLName, '
	SET @SQLString = @SQLString + 'Size '
	SET @SQLString = @SQLString + 'FROM Uv_ApplyFilterFile (NOLOCK) '
	SET @SQLString = @SQLString + @SQLText + ' '
	SET @SQLString = @SQLString + 'ORDER BY FileId '

	EXEC SP_EXECUTESQL @SQLString, @SQLParms

    IF @@ERROR <> 0
    BEGIN
        SET @ERROR_MSG = 'ERROR: Unable to apply file filter'
        GOTO EXIT_ERROR
    END

EXIT_PROC:
    SET NOCOUNT OFF
    RETURN 0

EXIT_ERROR:
    SET NOCOUNT OFF
    RAISERROR(@ERROR_MSG, 16, 1)
    RETURN -1
GO

/****** Object:  StoredProcedure [dbo].[Up_FilterApplyFileCount]    Script Date: 07/06/2006 09:51:47 ******/
CREATE PROCEDURE [dbo].[Up_FilterApplyFileCount] (
    @SQLText    NVARCHAR(3600)
)
AS

    SET NOCOUNT ON

	DECLARE @ERROR_MSG          VARCHAR (255),
			@SQLParms           NVARCHAR(512),
			@SQLString          NVARCHAR(4000),
			@TotalFileCount     INT,
			@CreatedFileCount   INT

	SELECT @TotalFileCount = COUNT(*) FROM omFile

	SET @SQLParms = '@CreatedFileCount INT OUT'
	SET @SQLString = 'SELECT @CreatedFileCount = COUNT(AF.FileId) '
	SET @SQLString = @SQLString + 'FROM omActionFile AF (NOLOCK) '
	If (@SQLText <> '')
	Begin
		SET @SQLString = @SQLString + 'INNER JOIN (SELECT DISTINCT FileId FROM Uv_ApplyFilterFile (NOLOCK) '
		SET @SQLString = @SQLString + @SQLText
		SET @SQLString = @SQLString + ') X  On X.FileId = AF.FileId'
	End

	EXEC SP_EXECUTESQL @SQLString, @SQLParms, @CreatedFileCount OUT

    IF @@ERROR <> 0
    BEGIN
        SET @ERROR_MSG = 'ERROR: Unable to get file counts'
        GOTO EXIT_ERROR
    END


	SET @SQLParms = '@TotalFileCount INT, @CreatedFileCount INT'
	SET @SQLString = 'SELECT @TotalFileCount AS TotalFileCount, '
	SET @SQLString = @SQLString + 'COUNT(DISTINCT FileId) AS FileCount, '
	SET @SQLString = @SQLString + 'COUNT(DISTINCT DNS + '':'' + ComputerName) AS ComputerCount, '
	SET @SQLString = @SQLString + '@CreatedFileCount AS CreatedFileCount '
	SET @SQLString = @SQLString + 'FROM Uv_ApplyFilterFile (NOLOCK) '
	SET @SQLString = @SQLString + @SQLText

	EXEC SP_EXECUTESQL @SQLString, @SQLParms, @TotalFileCount, @CreatedFileCount

    IF @@ERROR <> 0
    BEGIN
        SET @ERROR_MSG = 'ERROR: Unable to get file counts'
        GOTO EXIT_ERROR
    END

EXIT_PROC:
    SET NOCOUNT OFF
    RETURN 0

EXIT_ERROR:
    SET NOCOUNT OFF
    RAISERROR(@ERROR_MSG, 16, 1)
    RETURN -1
GO


/****** Object:  StoredProcedure [dbo].[Up_FilterApplyComputer]    Script Date: 07/25/2006 11:32:14 ******/
CREATE PROCEDURE [dbo].[Up_FilterApplyComputer] (
    @SQLText    NVARCHAR(3600),
	@Records    INT = 1000
)
AS

    SET NOCOUNT ON

	DECLARE @ERROR_MSG      VARCHAR (255),
			@SQLParms       NVARCHAR(512),
			@SQLString      NVARCHAR(4000)

	SET @Records = ISNULL(@Records, 1000)

	SET @SQLParms = ''
	SET @SQLString = 'SELECT '

	IF @Records > 0
	BEGIN
		SET @SQLString = @SQLString + 'TOP '+ CONVERT(NVARCHAR(16), @Records) +' '
	END

	SET @SQLString = @SQLString + 'F.DNS, '
	SET @SQLString = @SQLString + 'F.ComputerName, '
	SET @SQLString = @SQLString + 'COUNT(DISTINCT F.FileId) TotalFiles, '
	SET @SQLString = @SQLString + 'SUM(CASE F.MaxIssueLevel WHEN 1 THEN 1 ELSE 0 END) AS RedFiles, '
	SET @SQLString = @SQLString + 'SUM(CASE F.MaxIssueLevel WHEN 2 THEN 1 ELSE 0 END) AS YellowFiles, '
	SET @SQLString = @SQLString + 'SUM(CASE F.MaxIssueLevel WHEN 3 THEN 1 ELSE 0 END) AS GreenFiles, '
	SET @SQLString = @SQLString + 'SUM(CASE FI.IssueId WHEN 2000 THEN 1 ELSE 0 END) AS ConvertedFiles '
	SET @SQLString = @SQLString + 'FROM omFile F (NOLOCK) '

	If (@SQLText <> '')
	Begin
		SET @SQLString = @SQLString + 'INNER JOIN (SELECT DISTINCT FileId FROM Uv_ApplyFilterFile ' + @SQLText + ') X ON X.FileId = F.FileId '
	End

	SET @SQLString = @SQLString + 'LEFT JOIN omFileIssue FI (NOLOCK) ON FI.FileId = F.FileId AND FI.IssueId = 2000 AND FI.IsResolved = 1 '
	SET @SQLString = @SQLString + 'GROUP BY F.DNS, F.ComputerName'


	EXEC SP_EXECUTESQL @SQLString, @SQLParms

    IF @@ERROR <> 0
    BEGIN
        SET @ERROR_MSG = 'ERROR: Unable to apply computer filter'
        GOTO EXIT_ERROR
    END

EXIT_PROC:
    SET NOCOUNT OFF
    RETURN 0

EXIT_ERROR:
    SET NOCOUNT OFF
    RAISERROR(@ERROR_MSG, 16, 1)
    RETURN -1
GO


/****** Object:  StoredProcedure [dbo].[Up_FilterApplyIssue]    Script Date: 07/06/2006 18:59:27 ******/
CREATE PROCEDURE [dbo].[Up_FilterApplyIssue] (
    @SQLText    NVARCHAR(3600)
)
AS

    SET NOCOUNT ON

	DECLARE @ERROR_MSG      VARCHAR (255),
			@SQLParms       NVARCHAR(512),
			@SQLString      NVARCHAR(4000)


	SET @SQLParms = ''
	SET @SQLString = 'SELECT DISTINCT IL.IssueLevelId, '
	SET @SQLString = @SQLString + 'IL.Description AS IssueLevel, '
	SET @SQLString = @SQLString + 'I.IssueId, '
	SET @SQLString = @SQLString + 'I.Title AS Issue, '
	SET @SQLString = @SQLString + 'I.Description AS IssueDescription, '
	SET @SQLString = @SQLString + 'IT.Description AS IssueType, '
	SET @SQLString = @SQLString + 'FI.IsResolved AS Resolved, '
	SET @SQLString = @SQLString + 'COUNT(I.IssueId) AS IssueCount '
	SET @SQLString = @SQLString + 'FROM omFile F (NOLOCK) '

	If (@SQLText <> '')
	Begin
		SET @SQLString = @SQLString + 'INNER JOIN (SELECT DISTINCT FileId, IssueId FROM Uv_ApplyFilterFile ' + @SQLText + ') X ON X.FileId = F.FileId '
		SET @SQLString = @SQLString + 'INNER JOIN omFileIssue FI (NOLOCK) ON FI.FileId = F.FileId AND FI.IssueId = X.IssueId '
	End
	Else
	Begin
		SET @SQLString = @SQLString + 'INNER JOIN omFileIssue FI (NOLOCK) ON FI.FileId = F.FileId  '
	End

	SET @SQLString = @SQLString + 'INNER JOIN omIssue I (NOLOCK) ON I.IssueId = FI.IssueId '
	SET @SQLString = @SQLString + 'INNER JOIN omIssueLevel IL (NOLOCK) ON IL.IssueLevelId = I.IssueLevelId '
	SET @SQLString = @SQLString + 'INNER JOIN omIssueType IT (NOLOCK) ON IT.IssueTypeId = I.IssueTypeId '
	SET @SQLString = @SQLString + 'GROUP BY '
	SET @SQLString = @SQLString + 'IL.IssueLevelId, '
	SET @SQLString = @SQLString + 'IL.Description, '
	SET @SQLString = @SQLString + 'I.IssueId, '
	SET @SQLString = @SQLString + 'I.Title, '
	SET @SQLString = @SQLString + 'I.Description, '
	SET @SQLString = @SQLString + 'IT.Description,'
	SET @SQLString = @SQLString + 'FI.IsResolved '

	EXEC SP_EXECUTESQL @SQLString, @SQLParms

    IF @@ERROR <> 0
    BEGIN
        SET @ERROR_MSG = 'ERROR: Unable to apply issue filter'
        GOTO EXIT_ERROR
    END

EXIT_PROC:
    SET NOCOUNT OFF
    RETURN 0

EXIT_ERROR:
    SET NOCOUNT OFF
    RAISERROR(@ERROR_MSG, 16, 1)
    RETURN -1
GO

/****** Object:  StoredProcedure [dbo].[Up_FilterApplyCreatedFile]    Script Date: 07/06/2006 20:24:40 ******/
CREATE PROCEDURE [dbo].[Up_FilterApplyCreatedFile] (
    @SQLText    NVARCHAR(3600), 
	@Records    INT = 1000
)
AS

    SET NOCOUNT ON

	DECLARE @ERROR_MSG      VARCHAR (255),
			@SQLParms       NVARCHAR(512),
			@SQLString      NVARCHAR(4000)

	SET @Records = ISNULL(@Records, 1000)

	SET @SQLParms = ''
	SET @SQLString = 'SELECT DISTINCT '

	IF @Records > 0
	BEGIN
		SET @SQLString = @SQLString + 'TOP '+ CONVERT(NVARCHAR(16), @Records) +' '
	END

	SET @SQLString = @SQLString + 'AF.Domain AS ActionFileDomain, '
	SET @SQLString = @SQLString + 'T.Title AS ToolName, '
	SET @SQLString = @SQLString + 'A.ActionOptions, '
	SET @SQLString = @SQLString + 'FC.Description AS ActionFileCategory, '
	SET @SQLString = @SQLString + 'AF.ComputerName AS ActionComputerName, '
	SET @SQLString = @SQLString + 'AF.Name AS ActionFileName, '
	SET @SQLString = @SQLString + 'AF.Path AS ActionFilePath, '
	SET @SQLString = @SQLString + 'AF.ActionDate AS ActionDate,'
	SET @SQLString = @SQLString + 'F.ComputerName AS FileComputerName , '
	SET @SQLString = @SQLString + 'F.Name AS FileName, '
	SET @SQLString = @SQLString + 'F.Path AS FilePath, '
	SET @SQLString = @SQLString + 'FF.Description As FileType, '
	SET @SQLString = @SQLString + 'F.ModifiedDate AS FileModifiedDate, '
	SET @SQLString = @SQLString + 'F.FileId '
	SET @SQLString = @SQLString + 'FROM omFile F (NOLOCK) '

	If (@SQLText <> '')
	Begin
		SET @SQLString = @SQLString + 'INNER JOIN (SELECT DISTINCT FileId FROM Uv_ApplyFilterFile ' + @SQLText + ') X ON X.FileId = F.FileId '
	End

	SET @SQLString = @SQLString + 'INNER JOIN omAction A (NOLOCK) ON A.FileId = F.FileId '
	SET @SQLString = @SQLString + 'INNER JOIN omTool T (NOLOCK) ON T.ToolId = A.ToolId '
	SET @SQLString = @SQLString + 'INNER JOIN omActionFile AF (NOLOCK) ON (AF.FileId = A.FileId AND AF.ToolId = A.ToolId AND AF.ActionDate = A.ActionDate) '
	SET @SQLString = @SQLString + 'INNER JOIN omFileCategory FC (NOLOCK) ON FC.FileCategoryId = AF.FileCategoryId '
	SET @SQLString = @SQLString + 'INNER JOIN osFileFormat FF (NOLOCK) ON FF.FileFormatId = F.FileFormatId '

	EXEC SP_EXECUTESQL @SQLString, @SQLParms

    IF @@ERROR <> 0
    BEGIN
        SET @ERROR_MSG = 'ERROR: Unable to apply action file filter'
        GOTO EXIT_ERROR
    END

EXIT_PROC:
    SET NOCOUNT OFF
    RETURN 0

EXIT_ERROR:
    SET NOCOUNT OFF
    RAISERROR(@ERROR_MSG, 16, 1)
    RETURN -1
GO


/****** Object:  StoredProcedure [dbo].[Up_GetOMPMTableAndViewNames]    Script Date: 07/17/2006 11:04:32 ******/
CREATE PROCEDURE [dbo].[Up_GetOMPMTableAndViewNames]
AS
    SET NOCOUNT ON

	DECLARE 	@ERROR_MSG      VARCHAR (255)

	select TABLE_NAME as name from information_schema.Tables
	where 	(TABLE_TYPE = 'BASE TABLE') Or
		(TABLE_TYPE = 'VIEW')

    IF @@ERROR <> 0
    BEGIN
        SET @ERROR_MSG = 'ERROR: Unable to get OMPM Table and View names'
        GOTO EXIT_ERROR
    END

EXIT_PROC:
    SET NOCOUNT OFF
    RETURN 0

EXIT_ERROR:
    SET NOCOUNT OFF
    RAISERROR(@ERROR_MSG, 16, 1)
    RETURN -1
GO

-- Provisioned Data --
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (0, '[Undefined]')
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (1, 'File is Password Protected.')
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (2, 'Access Denied opening file.')
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (3, 'File Type Not Supported by OMPM Deep Scanner.')
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (4, 'File is IRM Protected.')
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (5, 'Unable to open file for scanning.')
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (6, 'The file path cannot be found.')
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10011, 'Config file missing Folders To Scan.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10012, 'Config file missing Folders To Exclude.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10098, 'A directory contains an invalid unicode character in its name.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10099, 'A directory contains an invalid unicode character in its name.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10101, 'Error reading physical memory.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10102, 'Error getting list of mapped drives.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10103, 'MS Jet not install on PC. Cannot scan any Access files.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10104, 'ScanMyDocuments value in config file is invalid (Valid values are 1 and 0).');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10105, 'ScanDesktop value in config file is invalid  (Valid values are 1 and 0).');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10106, 'Access Denied opening Folder.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10107, 'Path of file or folder is too long.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10108, 'Verbose value in config file is invalid (Valid values are 1 and 0).');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10109, 'CabLogs value in config file is invalid (Valid values are 1 and 0).');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10111, 'DeepScan value in config file is invalid(Valid values are 1 and 0).');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10112, 'Unrecognized line in OFFSCAN.INI');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10113, 'Folder Path not Found');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10114, 'RetryCount value in config file is invalid(Valid values are integers).');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10115, 'RetryInterval value in config file is invalid(Valid values are are integers).');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10116, 'Recovery value in config file is invalid(Valid values are 1 and 0).');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10117, 'LogOutput value in config file is invalid(Valid values are 1 and 0).');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10118, 'RetryTimeout value in config file is invalid(Valid values are are integers).');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10301, 'File access error: Access denied for file or folder.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10302, 'File access error: Network could not be reached.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10303, 'File access error: Password protected file or folder.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10304, 'File access error: Unknown file access issue.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (10305, 'File access error: File not found.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20001, 'Config file missing Access extentions.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20002, 'DAO properties option was selected, however DAO was not present on the machine.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20003, 'Error occured while scanning databases.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20004, 'You must have Microsoft Windows Script Runtime, a component of the Windows operating system, installed on your computer to use the Access Conversion Toolkit Scan tool.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20005, 'Unable to setup temporary directory.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20006, 'Access properties option was selected, however Access was not present on the machine.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20100, 'AutoExec macro exists in database. Access properties skipped.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20101, 'Digital Signature exists in database. Access properties skipped.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20102, 'Database not an Access database. Access properties skipped.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20103, 'Database cannot be opened by installed version of Access. Access properties skipped.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20104, 'Database is under source code control. Access properties skipped.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20105, 'This is a replica database and has unresolved conflicts. Access properties skipped.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20106, 'Database too large, not copying. Access properties skipped.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20107, 'Error deleting StartUpForm property. Access properties skipped.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20108, 'Not logging Access properties for database.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20109, 'Access timed out while scanning the database. Access properties skipped.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20110, 'Access crashed while scanning the database. Access properties skipped.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20111, 'Failed to write NoConvertDialog property.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20112, 'Could not open database through DAO.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20113, 'Could not open database through DAO: User Level Security.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20114, 'Could not open database through DAO: Database Password.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20115, 'Unable to copy database to temporary directory.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20116, 'Could not open copy of database through DAO for writing.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20117, 'Database made Access visible, skipping.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20118, 'Could not open database through Access.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20119, 'Could not open database through DAO for writing NoConvertDialog.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20120, 'Could not remove read only property from copied database. Access properties skipped.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20200, 'The Microsoft® Office Access Database Engine, required for a DAO level scan of .accdb, .accde, .accdu, .accda, and .accdr files, is not installed on this computer.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (20201, 'Template databases in the .accdt format cannot be scanned for DAO or Access level properties.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (30001, 'Config file missing Excel extentions.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (80001, 'Config file missing PowerPoint extentions.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (90001, 'Config file missing Project extentions.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (100011, 'Config file missing Publisher extentions.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (110011, 'Config file missing Visio extentions.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (120011, 'Config file missing Word extentions.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (140010, 'Error obtaining VBAMacroProject.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (140012, 'Error obtaining CertIssuedBy.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (140013, 'Error obtaining CertIssuedTo.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (140014, 'Error obtaining CertValidFrom.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (140015, 'Error obtaining CertValidTo.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (140016, 'Error obtaining SigTimeStampSigningTime.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (140017, 'Error obtaining SigTimeSTampSignerName.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (140018, 'Error obtaining CertSerialNum.');
INSERT INTO [dbo].[osErrorText] (ErrorID, ErrorDescription) VALUES (140019, 'Error obtaining VBA Project Signature information.');
GO


INSERT omCSIDL (CSIDL, Name) VALUES (-1, '[Undefined]')
INSERT omCSIDL (CSIDL, Name) VALUES (48, 'Admin Tools')
INSERT omCSIDL (CSIDL, Name) VALUES (29, 'Alt Startup')
INSERT omCSIDL (CSIDL, Name) VALUES (26, 'App Data')
INSERT omCSIDL (CSIDL, Name) VALUES (10, 'Bit Bucket')
INSERT omCSIDL (CSIDL, Name) VALUES (59, 'CD Burn Area')
INSERT omCSIDL (CSIDL, Name) VALUES (47, 'Common Admin Tools')
INSERT omCSIDL (CSIDL, Name) VALUES (30, 'Common Alt Startup')
INSERT omCSIDL (CSIDL, Name) VALUES (35, 'Common App Data')
INSERT omCSIDL (CSIDL, Name) VALUES (25, 'Common Desktop Directory')
INSERT omCSIDL (CSIDL, Name) VALUES (46, 'Common Documents')
INSERT omCSIDL (CSIDL, Name) VALUES (31, 'Common Favorites')
INSERT omCSIDL (CSIDL, Name) VALUES (53, 'Common Music')
INSERT omCSIDL (CSIDL, Name) VALUES (54, 'Common Pictures')
INSERT omCSIDL (CSIDL, Name) VALUES (23, 'Common Programs')
INSERT omCSIDL (CSIDL, Name) VALUES (22, 'Common Start Menu')
INSERT omCSIDL (CSIDL, Name) VALUES (24, 'Common Startup')
INSERT omCSIDL (CSIDL, Name) VALUES (45, 'Common Templates')
INSERT omCSIDL (CSIDL, Name) VALUES (55, 'Common Video')
INSERT omCSIDL (CSIDL, Name) VALUES (61, 'Computers Near Me')
INSERT omCSIDL (CSIDL, Name) VALUES (49, 'Connections')
INSERT omCSIDL (CSIDL, Name) VALUES (3,  'Controls')
INSERT omCSIDL (CSIDL, Name) VALUES (33, 'Cookies')
INSERT omCSIDL (CSIDL, Name) VALUES (0,  'Desktop')
INSERT omCSIDL (CSIDL, Name) VALUES (16, 'Desktop Directory')
INSERT omCSIDL (CSIDL, Name) VALUES (17, 'Drives')
INSERT omCSIDL (CSIDL, Name) VALUES (6,  'Favorites')
INSERT omCSIDL (CSIDL, Name) VALUES (20, 'Fonts')
INSERT omCSIDL (CSIDL, Name) VALUES (34, 'History')
INSERT omCSIDL (CSIDL, Name) VALUES (1,  'Internet')
INSERT omCSIDL (CSIDL, Name) VALUES (32, 'Internet Cache')
INSERT omCSIDL (CSIDL, Name) VALUES (28, 'Local App Data')
INSERT omCSIDL (CSIDL, Name) VALUES (12, 'My Documents')
INSERT omCSIDL (CSIDL, Name) VALUES (13, 'My Music')
INSERT omCSIDL (CSIDL, Name) VALUES (39, 'My Pictures')
INSERT omCSIDL (CSIDL, Name) VALUES (14, 'My Video')
INSERT omCSIDL (CSIDL, Name) VALUES (19, 'Network Neighborhood')
INSERT omCSIDL (CSIDL, Name) VALUES (18, 'Network')
INSERT omCSIDL (CSIDL, Name) VALUES (5,  'Personal')
INSERT omCSIDL (CSIDL, Name) VALUES (4,  'Printers')
INSERT omCSIDL (CSIDL, Name) VALUES (27, 'Print Neighborhood')
INSERT omCSIDL (CSIDL, Name) VALUES (40, 'Profile')
INSERT omCSIDL (CSIDL, Name) VALUES (38, 'Program Files')
INSERT omCSIDL (CSIDL, Name) VALUES (43, 'Program Files Common')
INSERT omCSIDL (CSIDL, Name) VALUES (2,  'Programs')
INSERT omCSIDL (CSIDL, Name) VALUES (8,  'Recent')
INSERT omCSIDL (CSIDL, Name) VALUES (56, 'Resources')
INSERT omCSIDL (CSIDL, Name) VALUES (9,  'Send To')
INSERT omCSIDL (CSIDL, Name) VALUES (11, 'Start Menu')
INSERT omCSIDL (CSIDL, Name) VALUES (7,  'Startup')
INSERT omCSIDL (CSIDL, Name) VALUES (37, 'System')
INSERT omCSIDL (CSIDL, Name) VALUES (21, 'Templates')
INSERT omCSIDL (CSIDL, Name) VALUES (36, 'Windows')
GO


INSERT INTO [dbo].[osFileFormat] (FileFormatID, Description) VALUES (1, 'Access');
INSERT INTO [dbo].[osFileFormat] (FileFormatID, Description) VALUES (2, 'Excel');
INSERT INTO [dbo].[osFileFormat] (FileFormatID, Description) VALUES (3, 'PowerPoint');
INSERT INTO [dbo].[osFileFormat] (FileFormatID, Description) VALUES (4, 'Project');
INSERT INTO [dbo].[osFileFormat] (FileFormatID, Description) VALUES (5, 'Publisher');
INSERT INTO [dbo].[osFileFormat] (FileFormatID, Description) VALUES (6, 'Visio');
INSERT INTO [dbo].[osFileFormat] (FileFormatID, Description) VALUES (7, 'Word');
INSERT INTO [dbo].[osFileFormat] (FileFormatID, Description) VALUES (8, 'Other');
GO


INSERT INTO [dbo].[omIssueLevel] (IssueLevelId, Description) VALUES (1, 'Red');
INSERT INTO [dbo].[omIssueLevel] (IssueLevelId, Description) VALUES (2, 'Yellow');
INSERT INTO [dbo].[omIssueLevel] (IssueLevelId, Description) VALUES (3, 'Green');
INSERT INTO [dbo].[omIssueLevel] (IssueLevelId, Description) VALUES (4, 'No Issues');
GO


INSERT INTO [dbo].[omIssueType] (IssueTypeId, Description, IsPromoted) VALUES (1, 'Upgrade Issue', 0);
INSERT INTO [dbo].[omIssueType] (IssueTypeId, Description, IsPromoted) VALUES (2, 'File Access Error', 1);
INSERT INTO [dbo].[omIssueType] (IssueTypeId, Description, IsPromoted) VALUES (3, 'Tool Error', 1);
INSERT INTO [dbo].[omIssueType] (IssueTypeId, Description, IsPromoted) VALUES (4, 'State Issue', 1);
INSERT INTO [dbo].[omIssueType] (IssueTypeId, Description, IsPromoted) VALUES (5, 'Scan Error', 1);
GO


INSERT INTO [dbo].[omFileCategory] (FileCategoryId, Description) VALUES (1000, 'Upgrade');
INSERT INTO [dbo].[omFileCategory] (FileCategoryId, Description) VALUES (1001, 'Backup');
INSERT INTO [dbo].[omFileCategory] (FileCategoryId, Description) VALUES (1010, 'Version Extraction');
GO


INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1000, 'File Deleted', 
	'The file no longer exists at the requested location.', 
	'http://technet2.microsoft.com/Office/en-us/library/0792e43a-3183-454a-8050-fe69790bf5c61033.mspx', 
	1, 2);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1001, 'File Access Error', 
	'The file location could not be accessed, probably because a machine was inaccessible.', 
	'http://technet2.microsoft.com/Office/en-us/library/0792e43a-3183-454a-8050-fe69790bf5c61033.mspx', 
	2, 2);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1002, 'File Modified', 
	'The file modified date did not match the modified date in the file list.', 
	'http://technet2.microsoft.com/Office/en-us/library/0792e43a-3183-454a-8050-fe69790bf5c61033.mspx', 
	1, 2);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1003, 'No Write Permissions', 
	'The user account does not have permissions to write to the file.', 
	'http://technet2.microsoft.com/Office/en-us/library/0792e43a-3183-454a-8050-fe69790bf5c61033.mspx', 
	2, 3);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1010, 'Not Deep Scanned', 
	'The file has not been deep scanned yet.', 
	'http://technet2.microsoft.com/Office/en-us/library/0792e43a-3183-454a-8050-fe69790bf5c61033.mspx', 
	2, 4);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1050, 'File Scan Error', 
	'An error occurred while scanning this file. Review the Scan Coverage and Errors report for more information.', 
	'http://technet2.microsoft.com/Office/en-us/library/0792e43a-3183-454a-8050-fe69790bf5c61033.mspx', 
	2, 3);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1100, 'Document contains versions', 
	'Edited versions of the document will be removed on opening the file in Word 2007, even in compatibility mode.', 
	'http://technet2.microsoft.com/Office/f/?en-us/library/e55b85c1-213f-47d5-809c-aba9331ae0331033.mspx', 
	1, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1200, 'Send for review data', 
	'This file has review comments and contains a hidden, baseline copy of the original. PowerPoint 2007 discards the hidden copy and saving removes it permanently. Users can''t tell which edits reviewers made if re-opened in previous versions.', 
	'http://technet2.microsoft.com/Office/f/?en-us/library/9f33abf2-99a8-4550-bebc-b4a8fbb1322b1033.mspx', 
	1, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1201, 'Embedded documents', 
	'There are potential performance, security and fidelity issues with embedded documents.', 
	'http://technet2.microsoft.com/Office/f/?en-us/library/9f33abf2-99a8-4550-bebc-b4a8fbb1322b1033.mspx', 
	2, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1202, 'VBA code', 
	'This file contains embedded VBA code. This can create security, fidelity, performance, and solution compatibility issues. Check this file for compatibility with PowerPoint 2007.', 
	'http://technet2.microsoft.com/Office/f/?en-us/library/9f33abf2-99a8-4550-bebc-b4a8fbb1322b1033.mspx', 
	2, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1203, 'Microsoft Script Editor data', 
	'When opening this file, PowerPoint 2007 discards MSE data that was stored on shapes, and saving removes it permanently. Solutions that depend on this data might break.', 
	'http://technet2.microsoft.com/Office/f/?en-us/library/9f33abf2-99a8-4550-bebc-b4a8fbb1322b1033.mspx', 
	1, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1204, 'Presentation broadcast data', 
	'When opening this file, PowerPoint 2007 discards configuration settings for HTML broadcast presentations, and saving removes it permanently. To broadcast in a previous version, the user must manually reenter the settings.', 
	'http://technet2.microsoft.com/Office/f/?en-us/library/9f33abf2-99a8-4550-bebc-b4a8fbb1322b1033.mspx', 
	1, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1205, 'Document routing slip', 
	'When opening this file, PowerPoint 2007 discards routing information, and saving removes it permanently. To route the presentation in an earlier version, the user must manually reenter the routing information. ', 
	'http://technet2.microsoft.com/Office/f/?en-us/library/9f33abf2-99a8-4550-bebc-b4a8fbb1322b1033.mspx', 
	1, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1206, 'Publish and subscribe data', 
	'When opening this file, PowerPoint 2007 discards Macintosh Publish and Subscribe information, and saving removes it permanently. If reopened in a previous version, the Publish and Subscribe feature will no longer function.', 
	'http://technet2.microsoft.com/Office/f/?en-us/library/9f33abf2-99a8-4550-bebc-b4a8fbb1322b1033.mspx', 
	2, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1207, 'Large number of OLE objects', 
	'This file contains a large number of embedded objects. This can create security, fidelity, performance, and solution compatibility issues. Check this file for compatibility with PowerPoint 2007.', 
	'http://technet2.microsoft.com/Office/f/?en-us/library/9f33abf2-99a8-4550-bebc-b4a8fbb1322b1033.mspx', 
	2, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1300, 'Open format not supported', 
	'This file format will not open in Excel 2007.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	1, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1301, 'Save format not supported', 
	'Excel 2007 does not support saving to this file format.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	2, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1302, 'HTML will be a publish-only file format.', 
	'The HTML file format will be a publish-only file format in Excel 2007. The file will open in Excel 2007, but on save to an Excel 2007 format, the file will be static.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	1, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1303, 'Links in workspace files may be broken', 
	'A workspace file (.xlw) may contain links to other workbooks. The .xlw file may be broken if the links are changed during an upgrade.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	3, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1304, 'File format is prior to Excel 97', 
	'File format is prior to Excel 97. Such files are not scanned for migration issues.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	2, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1305, 'SharePoint linked lists in the file', 
	'Linked lists are read-only in Excel 2007.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	2, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1306, 'Microsoft Script Editor present in the file', 
	'Microsoft Script Editor (MSE) has been removed in Excel 2007. There will be no UI access to MSE, and object model calls will return an error.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	1, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1307, 'Linked workbooks in the file', 
	'Linked workbooks are identified to help identify upgrade issues. The path to the linked workbook and the number of occurrences are identified. Linked workbooks will have different extensions when converted to the Excel 2007 file format.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	2, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1308, 'Charts in the workbook.', 
	'Charts might not render the same as Excel 2003 in Excel 2007.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	3, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1309, 'English Language Formulas in the workbook', 
	'English Language Formulas (ELFs) are turned on. ELFs have been removed in Excel 2007, but all ELFs will be changed to cell references so they can continue to work in Excel 2007.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	3, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1310, 'Embedded documents in the file', 
	'Embedded documents are not scanned for compatibility issues.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	2, 1);	
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1311, 'MSOWC.dll is referenced', 
	'This file uses features of the Office 2000 Web Components (MSOWC.dll). The Office 2000 Web Components will not be installed as part of Office 2007 and may need to be installed separately.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	3, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1312, 'OWC10.dll is referenced', 
	'This file uses features of the Office XP Web Components (OWC10.dll). The Office XP Web Components will not be installed as part of Office 2007 and may need to be installed separately.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	3, 1);
INSERT INTO [dbo].[omIssue] (IssueId, Title, Description, HelpURL, IssueLevelId, IssueTypeId) 
VALUES (1313, 'OWC11.dll is referenced', 
	'This file uses features of the Office 2003 Web Components (OWC11.dll). The Office 2003 Web Components will not be installed as part of Office 2007 and may need to be installed separately.', 
	'http://technet2.microsoft.com/Office/en-us/library/bee594b4-01b1-4d17-90ca-d43735a7382a1033.mspx', 
	3, 1);
GO


INSERT INTO [dbo].[AccessDatabasesRatingProperties] (RatingID, Rating) VALUES (1, 'Required');
INSERT INTO [dbo].[AccessDatabasesRatingProperties] (RatingID, Rating) VALUES (2, 'Likely');
INSERT INTO [dbo].[AccessDatabasesRatingProperties] (RatingID, Rating) VALUES (3, 'Unlikely');
INSERT INTO [dbo].[AccessDatabasesRatingProperties] (RatingID, Rating) VALUES (4, 'Note');
INSERT INTO [dbo].[AccessDatabasesRatingProperties] (RatingID, Rating) VALUES (5, 'None');
GO


INSERT INTO [dbo].[AccessVersionsProperties] (VersionCode, Version) VALUES ('0', 'Unknown');
INSERT INTO [dbo].[AccessVersionsProperties] (VersionCode, Version) VALUES ('2', 'Access 2.0');
INSERT INTO [dbo].[AccessVersionsProperties] (VersionCode, Version) VALUES ('06.68', 'Access 95');
INSERT INTO [dbo].[AccessVersionsProperties] (VersionCode, Version) VALUES ('07.53', 'Access 97');
INSERT INTO [dbo].[AccessVersionsProperties] (VersionCode, Version) VALUES ('08.50', 'Access 2000');
INSERT INTO [dbo].[AccessVersionsProperties] (VersionCode, Version) VALUES ('09.50', 'Access 2002');
GO


INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (1, 'Boolean');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (2, 'Byte');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (3, 'Integer');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (4, 'Long');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (5, 'Currency');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (6, 'Single');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (7, 'Double');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (8, 'Date');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (9, 'Binary');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (10, 'Text');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (11, 'Long Binary');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (12, 'Memo');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (15, 'GUID');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (16, 'BigInt');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (17, 'VarBinary');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (18, 'Char');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (19, 'Numeric');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (20, 'Decimal');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (21, 'Float');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (22, 'Time');
INSERT INTO [dbo].[AccessFieldTypeLookupProperties] (FieldType, FieldTypeFriendlyName) VALUES (23, 'Time Stamp');
GO


INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (1, 'Too many code or class modules', 'Required', 'Error', 1);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (2, 'Sort order and system language do not match', 'Likely', 'Warning', 2);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (3, 'Replicated database', 'Required', 'Warning', 1);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (4, 'Database is an MDE file', 'Required', 'Error', 1);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (5, 'DAO 2.5/3.5 compatibility layer', 'None', 'Note', 3);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (6, 'Microsoft Jet SQL help', 'None', 'Note', 4);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (7, 'Additional References', 'Likely', 'Warning', 2);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (8, 'Missing References', 'Likely', 'Warning', 2);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (9, 'Reserved Name in Form/Report/Macro', 'None', 'Note', 4);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (10, 'Linked Tables', 'Unlikely', 'Warning', 3);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (11, 'Database in uncompiled state', 'None', 'Note', 4);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (12, 'Backup database', 'None', 'Note', 4);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (13, 'Sample database', 'None', 'Note', 4);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (14, 'Old Database', 'None', 'Note', 4);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (15, 'Secured Database: User Level Security', 'Likely', 'Error', 2);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (16, 'Secured Database: Database Password', 'Likely', 'Error', 2);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (17, 'System Database', 'None', 'Note', 4);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (18, 'Unsupported legacy format','Likely','Warning',2);
INSERT INTO [dbo].[AccessIssuesProperties] (IssueId, IssueText, UserIntervention, IssueType, UserInterventionPriority) VALUES (19, 'Unsupported legacy format - forms, reports, and modules will be lost','Required','Error',1);
GO


INSERT INTO [dbo].[AccessQueriesTypeLookupProperties] (TypeID, TypeFriendlyName) VALUES (0, 'Select');
INSERT INTO [dbo].[AccessQueriesTypeLookupProperties] (TypeID, TypeFriendlyName) VALUES (16, 'Crosstab');
INSERT INTO [dbo].[AccessQueriesTypeLookupProperties] (TypeID, TypeFriendlyName) VALUES (32, 'Delete');
INSERT INTO [dbo].[AccessQueriesTypeLookupProperties] (TypeID, TypeFriendlyName) VALUES (48, 'Update');
INSERT INTO [dbo].[AccessQueriesTypeLookupProperties] (TypeID, TypeFriendlyName) VALUES (64, 'Append');
INSERT INTO [dbo].[AccessQueriesTypeLookupProperties] (TypeID, TypeFriendlyName) VALUES (80, 'Make Table');
INSERT INTO [dbo].[AccessQueriesTypeLookupProperties] (TypeID, TypeFriendlyName) VALUES (96, 'DDL');
INSERT INTO [dbo].[AccessQueriesTypeLookupProperties] (TypeID, TypeFriendlyName) VALUES (112, 'SQL Pass Through');
INSERT INTO [dbo].[AccessQueriesTypeLookupProperties] (TypeID, TypeFriendlyName) VALUES (128, 'Set Operation');
INSERT INTO [dbo].[AccessQueriesTypeLookupProperties] (TypeID, TypeFriendlyName) VALUES (144, 'SPT Bulk');
INSERT INTO [dbo].[AccessQueriesTypeLookupProperties] (TypeID, TypeFriendlyName) VALUES (160, 'Compound');
INSERT INTO [dbo].[AccessQueriesTypeLookupProperties] (TypeID, TypeFriendlyName) VALUES (224, 'Procedure');
INSERT INTO [dbo].[AccessQueriesTypeLookupProperties] (TypeID, TypeFriendlyName) VALUES (240, 'Action');
GO

INSERT INTO [dbo].[AccessBackupTokens] (Name) VALUES ('_bak')
INSERT INTO [dbo].[AccessBackupTokens] (Name) VALUES ('_copy_')
INSERT INTO [dbo].[AccessBackupTokens] (Name) VALUES ('backup')
INSERT INTO [dbo].[AccessBackupTokens] (Name) VALUES ('Copy (')
INSERT INTO [dbo].[AccessBackupTokens] (Name) VALUES ('Copy of')
INSERT INTO [dbo].[AccessSampleFiles] (Name) VALUES ('access9.mdb')
INSERT INTO [dbo].[AccessSampleFiles] (Name) VALUES ('foodmart')
INSERT INTO [dbo].[AccessSampleFiles] (Name) VALUES ('fpnwind')
INSERT INTO [dbo].[AccessSampleFiles] (Name) VALUES ('northwind')
INSERT INTO [dbo].[AccessSampleFiles] (Name) VALUES ('nwind')
INSERT INTO [dbo].[AccessSampleFiles] (Name) VALUES ('SOLUTION.MDB')
INSERT INTO [dbo].[AccessSampleFiles] (Name) VALUES ('SOLUTIONS.MDB')
INSERT INTO [dbo].[AccessSystemFiles] (Name) VALUES ('acwzlib')
INSERT INTO [dbo].[AccessSystemFiles] (Name) VALUES ('acwzmain')
INSERT INTO [dbo].[AccessSystemFiles] (Name) VALUES ('acwztool')
INSERT INTO [dbo].[AccessSystemFiles] (Name) VALUES ('acwzusr')
INSERT INTO [dbo].[AccessSystemFiles] (Name) VALUES ('wzlib80')
INSERT INTO [dbo].[AccessSystemFiles] (Name) VALUES ('wzmain80')
INSERT INTO [dbo].[AccessSystemFiles] (Name) VALUES ('wztool80')
GO