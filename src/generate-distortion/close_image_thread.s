// This DigitalMicrograph script is used to stop Smart Align from opening hundreds of image whilst doing the alignment
// In future versions of Smart Align it should be possible to disable the windows opening

class mythread : thread {

	object init(object self)
	{
		return self
	}

	void CloseAll(object self) {
		number kWINDOWTYPE_IMAGEWINDOW = 5
		number wsid = WorkspaceGetActive()
		number numberDocs = CountImageDocuments(wsid)
		number i
		//result(numberDocs + "\n")

		for(i = 0; i < numberDocs; ++ i)
		{
			ImageDocument imgDoc = GetImageDocument(0)
			image img := getfrontimage()

			imagedocumentClose(imgdoc, 0)
		}
	}
	
	void RunThread(object self) {

		while(1) {
			self.CloseAll()
			sleep(60)
		}

	}

}

alloc(mythread).init( ).StartThread( )