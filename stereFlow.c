#include <stdio.h>
#include <stdlib.h>

typedef unsigned char uint8;

void genStereFlow(float *pLeftFlow, float *pRightFlow, float *pDepth,  int h, int w)
{
    int i,j;
    float xl,xr, offset;
    int xl_i,xr_i;
    
    float *pFlow;
    float lastFlow;
    
    for(i = 0; i < h; i++)
    {
        for(j = 0; j < w; j++)
        {
            xl = j + pDepth[i*w+j];
            xr = j - pDepth[i*w+j];

            xl_i = xl;
            if(xl_i >= 0 && xl_i <= w-1)
            {
                offset = xl - xl_i;
                pLeftFlow[i*w+xl_i] = j - offset;
            }
            
            xr_i = xr;
            if(xr_i >= 0 && xr_i <= w-1)
            {
                offset = xr - xr_i;
                pRightFlow[i*w+xr_i] = j - offset;
            }
        }
        
        //Fill blank holes
        lastFlow = 0;
        pFlow =  pLeftFlow + i*w;
        for(j = 0; j < w; j++)
        {
            if(pFlow[j] == 0)
                pFlow[j] = lastFlow;
            else
                lastFlow = pFlow[j];
        }
        
        lastFlow = 0;
        pFlow = pRightFlow + i*w;
        for(j = w-1; j >= 0; j--)
        {
            if(pFlow[j] == 0)
                pFlow[j] = lastFlow;
            else
                lastFlow = pFlow[j];
        }
    }
}

void warpFlow(uint8 *pOut, uint8 *pImg, float *pFlow, int h, int w)
{
    int i,j;
    float xf, offset;
    int xi;
    
    for(i = 0; i < h; i++)
    {
        for(j = 0; j < w; j++)
        {
            xf = pFlow[i*w+j];
            xi = (int)xf;
            offset = xf - xi;
            if(xi > 0 && xi <= w-2)
            {
                pOut[(i*w+j)*3+0] = pImg[(i*w+xi)*3+0]*(1-offset) + pImg[(i*w+xi+1)*3+0]*offset;
                pOut[(i*w+j)*3+1] = pImg[(i*w+xi)*3+1]*(1-offset) + pImg[(i*w+xi+1)*3+1]*offset;
                pOut[(i*w+j)*3+2] = pImg[(i*w+xi)*3+2]*(1-offset) + pImg[(i*w+xi+1)*3+2]*offset;
            }
            else
            {
                pOut[(i*w+j)*3+0] = 0;
                pOut[(i*w+j)*3+1] = 0;
                pOut[(i*w+j)*3+2] = 0;
            }
        }
    }
}
