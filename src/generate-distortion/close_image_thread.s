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
			sleep(115)
			result("Closing all images in 5...\n")
			sleep(1)
			result("Closing all images in 4...\n")
			sleep(1)
			result("Closing all images in 3...\n")
			sleep(1)
			result("Closing all images in 2...\n")
			sleep(1)
			result("Closing all images in 1...\n")
			sleep(1)
			result("Closing all images NOW\n")
		}

	}

}

alloc(mythread).init( ).StartThread( )