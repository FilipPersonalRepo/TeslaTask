USE [TeslaTask]
GO

/****** Object:  StoredProcedure [dbo].[UpdateTables]    Script Date: 11/23/2023 11:34:52 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [dbo].[UpdateTables] @TableNameGE NVARCHAR(128), @TableNameJ NVARCHAR(128), @TableNameAT NVARCHAR(128)
AS
BEGIN
    DECLARE @Sql NVARCHAR(MAX);

    -- Log: Procedure start
    PRINT 'DROPPING TABLE IF EXISTS ' + @TableNameGE;

    SET @Sql = 'DROP TABLE IF EXISTS ' + QUOTENAME(@TableNameGE) + ';';
    EXEC sp_executesql @Sql;

    PRINT 'CREATING TABLE ' + @TableNameGE;
    SET @Sql = 'CREATE TABLE ' + QUOTENAME(@TableNameGE) + '(
        [Applicant ID] [bigint] NULL,
        [Gender] [varchar](max) NULL,
        [Ethnicity] [varchar](max) NULL
    ) ON [PRIMARY];';
    EXEC sp_executesql @Sql;

    PRINT 'INSERTING UNIQUE VALUES INTO ' + @TableNameGE;
    SET @Sql = 'INSERT INTO ' + QUOTENAME(@TableNameGE) + ' ([Applicant ID], [Gender], [Ethnicity])

		SELECT [Applicant ID], [Gender], [Ethnicity]
		FROM (
			SELECT *
			, ROW_NUMBER() OVER (PARTITION BY [Applicant ID] ORDER BY Ethnicity) AS rnk
			FROM [dbo].gender_ethnicity
		) x
		WHERE rnk = 1;
		'
    EXEC sp_executesql @Sql;
	--=================================================================
	PRINT 'DROPPING TABLE IF EXISTS ' + @TableNameJ;

    SET @Sql = 'DROP TABLE IF EXISTS ' + QUOTENAME(@TableNameJ) + ';';
    EXEC sp_executesql @Sql;

    PRINT 'CREATING TABLE ' + @TableNameJ;
    SET @Sql = 'CREATE TABLE ' + QUOTENAME(@TableNameJ) + '(
								[Department Code] [bigint] NULL,
								[Job Position Code] [bigint] NULL,
								[Pay Rate Type] [varchar](max) NULL
							) ON [PRIMARY];';
    EXEC sp_executesql @Sql;

    PRINT 'INSERTING UNIQUE VALUES INTO ' + @TableNameJ;
    SET @Sql = 'INSERT INTO ' + QUOTENAME(@TableNameJ) + ' ([Department Code], [Job Position Code], [Pay Rate Type])

					SELECT
						[Department Code],
						[Job Position Code],
						CASE
							WHEN COUNT(DISTINCT [Pay Rate Type]) = 2 THEN ''Both''
							WHEN MAX(CASE WHEN [Pay Rate Type] = ''Hourly'' THEN 1 ELSE 0 END) = 1 THEN ''Hourly''
							WHEN MAX(CASE WHEN [Pay Rate Type] = ''Salary'' THEN 1 ELSE 0 END) = 1 THEN ''Salary''
		
						END AS [Pay Rate Type]
					FROM dbo.job  -- Replace with your actual table name
					GROUP BY
						[Department Code],
						[Job Position Code];
					'
    EXEC sp_executesql @Sql;
--===========================================================================
    PRINT 'DROPPING TABLE IF EXISTS ' + @TableNameAT;

    SET @Sql = 'DROP TABLE IF EXISTS ' + QUOTENAME(@TableNameAT) + ';';
    EXEC sp_executesql @Sql;

    PRINT 'CREATING TABLE ' + @TableNameAT;
    SET @Sql = 'CREATE TABLE ' + QUOTENAME(@TableNameAT) + '(
	[Date Applied] [varchar](max) NULL,
	[Applicant ID] [bigint] NULL,
	[STAGE] [varchar](max) NULL,
	[Job Level] [varchar](max) NULL,
	[Department Code] [bigint] NULL,
	[Job Position Code] [bigint] NULL,
	[Target Start Date] [varchar](max) NULL,
	[Gender] varchar(50) NULL,
	[Ethnicity] varchar(50) NULL,
	[Pay Rate Type] varchar(50) NULL,

) ON [PRIMARY];';
    EXEC sp_executesql @Sql;

    PRINT 'INSERTING UNIQUE VALUES INTO ' + @TableNameAT;
    SET @Sql = 'INSERT INTO ' + QUOTENAME(@TableNameAT) + ' 		
				select r.*
					, ge.Gender
					, ge.Ethnicity
					, j.[Pay Rate Type]
				from dbo.raw_data r
				left join  ' + QUOTENAME(@TableNameJ) + '  j
					on j.[Job Position Code] = r.[Job Position Code] and j.[Department Code] = r.[Department Code]
				left join' + QUOTENAME(@TableNameGE) + ' ge
					on ge.[Applicant ID] = r.[Applicant ID]
'
    EXEC sp_executesql @Sql;
	
	PRINT 'DONE';
END;
GO


