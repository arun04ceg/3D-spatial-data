import vtk
import sys

OPACITY_POINTS = [(10, 0.0), (80, 0.2), (115, 0.5), (255, 0.0)]

COLOR_VALUES = [(0.0, 0.8, 0.8, 0.8), (60, 0.7, 0.7, 0.7), (100, 1, 1, 1), (110, 1, 1, 1)]

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

    MIPFunction = vtk.vtkVolumeRayCastMIPFunction()

    volumeMapper = vtk.vtkVolumeRayCastMapper()
    volumeMapper.SetSampleDistance(1.0)
    volumeMapper.SetInput(reader.GetOutput())
    volumeMapper.SetVolumeRayCastFunction(MIPFunction)

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
    renderer.SetBackground(0, 0, 0)
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
