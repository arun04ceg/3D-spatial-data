import vtk
import sys

OPACITY_POINTS = [(0, 0.0), (60, 0), (70, 0.05), (80, 0.2), (95, 0.2), (100, 0.0), (110, 0.0), (115, 0.6), (255, 0.6)]
COLOR_VALUES = [(0.0, 0.0, 0.0, 0.0), (60.0, 0.8, 0.2, 0.2), (100.0, 0.8, 0.2, 0.2), (110.0, 0.9, 0.9, 0.9), (120, 1, 1, 1)]
'''
OPACITY_POINTS = [(0, 0.0), (60, 0), (70, 0.05), (80, 0.2), (95, 0.2)]
COLOR_VALUES = [(0.0, 0.0, 0.0, 0.0), (60.0, 0.8, 0.2, 0.2), (100.0, 0.8, 0.2, 0.2)]
'''
def main(filename):
    reader = read_file(filename)
    opacityTransferFunction = set_opacity_transfer()
    colorTransferFunction = set_color_transfer()
    volume = volumeProperty(reader, opacityTransferFunction, colorTransferFunction)
    render(volume)

def read_file(filename):
    reader = vtk.vtkStructuredPointsReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader

def set_opacity_transfer():
    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    for each_point in OPACITY_POINTS:
        opacityTransferFunction.AddPoint(each_point[0], each_point[1])
    return opacityTransferFunction

def set_color_transfer():
    colorTransferFunction = vtk.vtkColorTransferFunction()
    for each_color in COLOR_VALUES:
        colorTransferFunction.AddRGBPoint(each_color[0], each_color[1], each_color[2], each_color[3])
    return colorTransferFunction

def volumeProperty(reader, opacityTransferFunction, colorTransferFunction):
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetSpecular(0.3)
    volumeProperty.SetInterpolationTypeToLinear()

    rayCastFunction = vtk.vtkVolumeRayCastCompositeFunction()

    volumeMapper = vtk.vtkVolumeRayCastMapper()
    volumeMapper.SetSampleDistance(1)
    volumeMapper.SetInput(reader.GetOutput())
    volumeMapper.SetVolumeRayCastFunction(rayCastFunction)

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    volume.RotateX(-90)
    return volume

def render(volume):
    renderer = vtk.vtkRenderer()
	
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(512, 512)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    renderer.AddVolume(volume)
    renderer.SetBackground(0.5, 0.5, 0.5)
    renderer.ResetCamera()

    style = vtk.vtkInteractorStyleTrackballCamera()
    interactor.SetInteractorStyle(style)

    renderWindow.Render()
    interactor.Start()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Format to execute: 'python %s <mummy filename>.vtk'" %(sys.argv[0])
        print "Exiting..."
        sys.exit(2)
    main(sys.argv[1])
