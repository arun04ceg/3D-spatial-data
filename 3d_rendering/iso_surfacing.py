import vtk
import sys

SKIN_BONE_LIST = [[(0, 70), (0.7, 0.2, 0.2), 0.4], [(0, 125), (0.9, 0.9, 1.0), 1]]

#SKIN_BONE_LIST = [[(0, 80), (0.7, 0.2, 0.2), 0.4], ]

def main(filename):
    reader = read_file(filename)
    actors_list = create_actors_for_skin_and_bone(reader)
    render(actors_list)

def read_file(filename):
    reader = vtk.vtkStructuredPointsReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader

def create_actors_for_skin_and_bone(reader):
    actors_list = []
    for contour_val, color, opacity in SKIN_BONE_LIST:
	contour = vtk.vtkContourFilter()
	contour.SetInput(reader.GetOutput())
	contour.SetNumberOfContours(1)
	contour.SetValue(contour_val[0], contour_val[1])

	normals = vtk.vtkPolyDataNormals()
	normals.SetInput(contour.GetOutput())
	normals.SetFeatureAngle(60)
	normals.ConsistencyOff()
	normals.SplittingOff()

	mapper = vtk.vtkPolyDataMapper()
	mapper.SetInput(normals.GetOutput())
	mapper.ScalarVisibilityOff()

	actor = vtk.vtkActor()
	actor.SetMapper(mapper)
	actor.GetProperty().SetColor(color)
        actor.GetProperty().SetOpacity(opacity)
	actor.RotateX(-90)
        actors_list.append(actor)
    return actors_list

def render(actors_list):
    renderer = vtk.vtkRenderer()

    renderWindow = vtk.vtkRenderWindow()	
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(512, 512)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    renderer.AddActor(actors_list[0])
    renderer.AddActor(actors_list[1])
    renderer.SetBackground(0.5, 0.5, 0.5)
    renderer.ResetCamera()

    renderWindow.Render()
    interactor.Start()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Format to execute: 'python %s <mummy filename>.vtk'" %(sys.argv[0])
        print "Exiting..."
        sys.exit(2)
    main(sys.argv[1])
