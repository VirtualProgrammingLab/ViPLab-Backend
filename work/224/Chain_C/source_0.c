
#include <stdio.h>
#include <stdlib.h>

// line types for graph lines
typedef enum
{
     solid = 0, dashed = 1, dotted = 2, dashdot = 3
} linetype;

// axis scale
typedef enum
{
     linear = 0, logarithmic = 1
} scaletype;

// valid symbols
char symbols[] = {' ', '.', 'x', '+', '*', 'v', '^', 'o', 's', 'd'};

/****************************************************************
 * plot graph to current frame                                  *
 ****************************************************************/
void viplab_plot_graph_2d(char symbol, linetype line,
                          size_t color_r, size_t color_g, size_t color_b, 
                          double* element_coords, size_t element_count, char* legend)
{
	// file handle to write to ViPLab plot file (vpf)
	FILE* plot_file;
	plot_file = fopen("vipplot.vgf", "a+");
	
	// write plot formatting
	fprintf(plot_file, "# color %zd %zd %zd\n", color_r, color_g, color_b);
	
	if (symbol == ' ')
	{
		fprintf(plot_file, "# symbol none\n");
	}
	else
	{
		fprintf(plot_file, "# symbol %c\n", symbol);
	}
	
	switch (line)
	{
		case solid:
			fprintf(plot_file, "# linestyle solid\n");
			break;
		case dashed:
			fprintf(plot_file, "# linestyle dashed\n");
			break;
		case dotted:
			fprintf(plot_file, "# linestyle dotted\n");
			break;
		case dashdot:
			fprintf(plot_file, "# linestyle dash-dot\n");
			break;
	}
	
	if (legend != NULL)
	{
		fprintf(plot_file, "# legend %s\n", legend);
	}
	
	// write plot data
	size_t coords_per_element = 4;
	for (int i = 0; i < element_count*coords_per_element; i += coords_per_element)
	{
		for (int j = 0; j + 1 < coords_per_element; j++)
		{
			fprintf(plot_file, "%lf ", element_coords[i + j]);
		}
		fprintf(plot_file, "%lf\n", element_coords[i + coords_per_element - 1]);
	}
	
	// close stream
	fclose(plot_file);
}

/****************************************************************
 * create a new frame, arguments which are NULL are ignored     *
 ****************************************************************/
void viplab_plot_new_frame(char* title, char* label_x, char* label_y,
                           scaletype scale_x, scaletype scale_y)
{
	// file handle to write to ViPLab plot file (vpf)
	FILE* plot_file;
	plot_file = fopen("vipplot.vgf", "a+");
	
	fprintf(plot_file, "# newframe");
	
	// write plot formatting
	if (title != NULL)
	{
		fprintf(plot_file, "# title %s\n", title);
	}
	if (label_x != NULL)
	{
		fprintf(plot_file, "# x-label %s\n", label_x);
	}
	if (label_y != NULL)
	{
		fprintf(plot_file, "# y-title %s\n", label_y);
	}
	
	fprintf(plot_file, "# scale ");
	if ((scale_x == linear) && (scale_y == logarithmic))
	{
		fprintf(plot_file, "lin-");
	}
	else if (scale_x == logarithmic)
	{
		fprintf(plot_file, "log-");
	}
	if ((scale_y == linear) && (scale_x == logarithmic))
	{
		fprintf(plot_file, "lin\n");
	}
	else if (scale_y == logarithmic)
	{
		fprintf(plot_file, "log\n");
	}
	
	// close stream
	fclose(plot_file);
}

// create a new frame. Arguments which are NULL are ignored
void viplab_frame_limits(double min_x, double max_x, double min_y, double max_y)
{
	// file handle to write to ViPLab plot file (vpf)
	FILE* plot_file;
	plot_file = fopen("vipplot.vgf", "a+");
	
	if (min_x < max_x)
	{
		fprintf(plot_file, "# x-range %lf %lf\n", min_x, max_x);
	}
	
	if (min_y < max_y)
	{
		fprintf(plot_file, "# y-range %lf %lf\n", min_y, max_y);
	}
	
	// close stream
	fclose(plot_file);
}





/*********************************************************************
 *                Testcode, nicht mehr Teil der Bibliothek           *
 *********************************************************************/
int main(void)
{
    printf("Hallo Welt\n");
    
    double points[] = {1.0, 2.0, 3.0, 2.1, 3.0, 2.1, 4.0, -1.1, 0.0, 1, 1.0, 2};
    viplab_plot_graph_2d('d', solid, 0, 0, 0, points, 3, "plot A");
    double points2[] = {1.0, 12.0, 2.0, -2.1};
    viplab_plot_graph_2d(' ', solid, 20, 40, 200, points2, 1, NULL);
    double points3[] = {1.0, 12.0, 2.0, -2.1, 1.0, 11.0, 2.0, -1.1};
    viplab_plot_graph_2d('*', solid, 255, 0, 255, points3, 2, "plot C");
    
    return EXIT_SUCCESS;
}
