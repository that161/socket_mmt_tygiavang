create database Socket
go

use Socket
go

CREATE TABLE TaiKhoan(
	[TenDangNhap] [varchar](50) NOT NULL,
	[MatKhau] [varchar](50) NOT NULL,
)

CREATE TABLE GiaVang(
	[TenVang] [nvarchar](30) NOT NULL,
	[GiaMua] [varchar](15) NOT NULL,
	[GiaBan] [varchar](15) NOT NULL,
	[Ngay] [varchar] (15) NULL,
)


GO
INSERT [dbo].[TaiKhoan] ([TenDangNhap], [MatKhau]) VALUES (N'abc', N'123')
INSERT [dbo].[TaiKhoan] ([TenDangNhap], [MatKhau]) VALUES (N'alo', N'123')
INSERT [dbo].[TaiKhoan] ([TenDangNhap], [MatKhau]) VALUES (N'that', N'123')
INSERT [dbo].[TaiKhoan] ([TenDangNhap], [MatKhau]) VALUES (N'hcmus1', N'123')
INSERT [dbo].[TaiKhoan] ([TenDangNhap], [MatKhau]) VALUES (N'hcmus2', N'123')

GO

INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'DOJI HN', N'60,700', N'61,600', N'16-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'DOJI SG', N'60,900', N'61,700', N'16-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'SJC TP HCM', N'58,800', N'59,500', N'16-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'SJC Hà Nội', N'59,800', N'60,520', N'16-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'SJC Đà Nẵng', N'59,800', N'60,620', N'16-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'PNJ TP.HCM', N'51,300', N'52,100', N'16-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'PNJ HN', N'51,300', N'52,100', N'16-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'DOJI HN', N'60,700', N'61,600', N'17-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'DOJI SG', N'60,900', N'61,700', N'17-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'SJC TP HCM', N'58,800', N'59,500', N'17-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'SJC Hà Nội', N'59,800', N'60,520', N'17-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'SJC Đà Nẵng', N'59,800', N'60,620', N'17-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'PNJ TP.HCM', N'51,300', N'52,100', N'17-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'PNJ HN', N'51,300', N'52,100', N'17-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'DOJI HN', N'60,700', N'61,600', N'18-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'DOJI SG', N'60,900', N'61,700', N'18-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'SJC TP HCM', N'58,800', N'59,500', N'18-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'SJC Hà Nội', N'59,800', N'60,520', N'18-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'SJC Đà Nẵng', N'59,800', N'60,620', N'18-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'PNJ TP.HCM', N'51,300', N'52,100', N'18-12-2021')
INSERT [dbo].[GiaVang] ([TenVang],[GiaMua],[GiaBan], [Ngay]) VALUES (N'PNJ HN', N'51,300', N'52,100', N'18-12-2021')

GO
ALTER DATABASE [Socket] SET  READ_WRITE 
GO