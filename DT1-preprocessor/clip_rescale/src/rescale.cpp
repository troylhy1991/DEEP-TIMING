#include "helpers.h"
#include "itkRescaleIntensityImageFilter.h"
#include "itkMedianImageFilter.h"

using namespace helpers;
template <typename T>
typename T::Pointer readImage(const char *filename)
{
	printf("Reading %s ... \n",filename);
	typedef typename itk::ImageFileReader<T> ReaderType;
	typename ReaderType::Pointer reader = ReaderType::New();

	ReaderType::GlobalWarningDisplayOff();
	reader->SetFileName(filename);
	try
	{
		reader->Update();
	}
	catch(itk::ExceptionObject &err)
	{
		std::cerr << "ExceptionObject caught!" <<std::endl;
		std::cerr << err << std::endl;
		//return EXIT_FAILURE;
	}
	printf("Done\n");
	return reader->GetOutput();

}
template <typename T>
int writeImage(typename T::Pointer im, const char* filename)
{
	printf("Writing %s ... \n",filename);
	typedef typename itk::ImageFileWriter<T> WriterType;

	typename WriterType::Pointer writer = WriterType::New();
	writer->SetFileName(filename);
	writer->SetInput(im);
	try
	{
		writer->Update();
	}
	catch(itk::ExceptionObject &err)
	{
		std::cerr << "ExceptionObject caught!" <<std::endl;
		std::cerr << err << std::endl;
		return EXIT_FAILURE;
	}
	return EXIT_SUCCESS;
}

template <typename T>
typename T::Pointer createImage( itk::Size<3> size )
{
    typename T::Pointer imageLabelMontage = T::New();
    typename T::PointType originz;
    originz[0] = 0;
    originz[1] = 0;
    originz[2] = 0;
    imageLabelMontage->SetOrigin( originz );
    typename T::IndexType indexStich;
    indexStich.Fill(0);
    typename T::RegionType regionz;
    regionz.SetSize ( size  );
    regionz.SetIndex( indexStich );
    imageLabelMontage->SetRegions( regionz );
    imageLabelMontage->Allocate();
    imageLabelMontage->FillBuffer(0);
    try
    {
        imageLabelMontage->Allocate();
    }
    catch(itk::ExceptionObject &err)
    {
        std::cerr << "ExceptionObject caught!" <<std::endl;
        std::cerr << err << std::endl;
    }
    return imageLabelMontage;
}


#define MAX_TIME 1000
bool file_exists(char *filename)
{
	FILE * fp = fopen(filename,"r");
	if(fp!=NULL)
	{
		fclose(fp);
		return true;
	}
	return false;
}

int main(int argc, char**argv)
{

	std::cout<<"number of arguments is: "<<argc<<std::endl;
	if(argc <7)
	{
		std::cout<<"Usage: rescale <InputImageFileName> <OutputImageFileName> <mix_pixel_value 0> <max_pixel_value 3000> <mix_clip_value 100> <max_clip_value 1000>\n";
		return 0;
	}
	
	int minPixelValue = atoi(argv[3]);
	int maxPixelValue = atoi(argv[4]);
	
	int minClipValue = atoi(argv[5]);
	int maxClipValue = atoi(argv[6]);
	
	std::string fname01 = argv[1];
	std::string fname02 = argv[2];
	
	std::cout<<"Input file name is: "<<fname01<<std::endl;
 	std::cout<<"Output file name is: "<<fname02<<std::endl;
	
	// Read the Input Image
	InputImageType16::Pointer inputImage01 = readImage<InputImageType16>(fname01.c_str());
	
	// Get the Image Information
	size_t numRows=inputImage01->GetLargestPossibleRegion().GetSize()[0];
	size_t numCols=inputImage01->GetLargestPossibleRegion().GetSize()[1];
	size_t numTimes=inputImage01->GetLargestPossibleRegion().GetSize()[2];

	InputPixelType16 * inputImage01Ptr = inputImage01->GetBufferPointer();
	
	// clip the pixel value
	size_t nPixels = (numRows*numCols*numTimes);

	
	for(size_t index=0; index<nPixels; ++index)
	{	

		int inVal01 = (int) inputImage01Ptr[index];
		if(inVal01 > maxClipValue){inVal01 = maxClipValue;}
		if(inVal01 < minClipValue){inVal01 = 0;}
		
    inputImage01Ptr[index] = (InputPixelType16) inVal01;
	}
	
	// Rescale the Image
	typedef itk::RescaleIntensityImageFilter< InputImageType16, OutputImageType16 > RescaleFilterType;
	RescaleFilterType::Pointer rescaleFilter = RescaleFilterType::New();
	rescaleFilter->SetInput(inputImage01);
	rescaleFilter->SetOutputMinimum(minPixelValue);
	rescaleFilter->SetOutputMaximum(maxPixelValue);	
	

	// Meidan Filter the Image
	//typedef itk::MedianImageFilter<InputImageType16, OutputImageType16> FilterType;
	//FilterType::Pointer medianFilter = FilterType::New();
	//FilterType::InputSizeType radius;
	//radius.Fill(2);

	//medianFilter->SetRadius(radius);
	//medianFilter->SetInput( rescaleFilter->GetOutput() );


	
	std::cout<< "Rescale done ........."<<std::endl;
	
	writeImage<InputImageType16>( rescaleFilter->GetOutput(),fname02.c_str() );

    std::cout << std::endl;
	
}