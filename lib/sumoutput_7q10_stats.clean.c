/*This program summarizes a group of daily time step routed streamflow files. 
and prints flood statistics from fitted GEV probability distributions estimated from the 
annual peak flow time series. The output is a file containing station info and flood stats (1 record per station) in order of processing*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

int main( int argc, char* argv[]){

	int    i, j, k, q;
	float  tempsort[100], sort[100][5];
	float  **last, sum7day[7000];
	float  strflw, **minvarsum, **minvaravg;
	double B[15], NB[15],UB[15], sum[15], L[5], LH2[5], LH4[5], tau23, tau24, tau43, tau44;
	double LN[2],lnsum[2], a2[5], a4[5], gammafunc;
	double  c, kappa[3], alpha[3], psi[3];
	float  p[10],zp, output[1000][5][10];
	float t1;
	FILE   *inputfile, *outputfile[10];
	char   name[7000][50], temp[100], inpathstr[100], outpathstr[100];
	int    year, mnth, day, begdatayear, startyear, endyear, date[3],numyears, sampsize, numcells;
	int    maxcells = 7000, maxyrs = 200, **wydminvar, **wydminmnth, **wydminday;
	int    icell, iyear, cmnth[12];
	int    calc_lmoments;
	int    endmnth, begdatamnth, begmnth;
	int    dpm[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
	int    jdm[12];
//	int    jdm1[12] = {0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334}; //calendar year
	int    jdm2[12] = {61,92,123,152,182,212,243,274,304,335,0,31}; //10-9 water year
	int    jdm3[12] = {61,92,123,153,183,213,244,274,305,336,0,31}; //10-9 water year leap years
	int    skipOn=1;
	int caldate[3], wymonth;
	int **m12check;


	void   shellsort(int n, float a[]);
	double gammafn2(float x);

	if(argc != 9){
		printf("Wrong command line arguments: enter churu <filelist> <inpath> <outpath> <begindatayear> <startyear> <endyear> <idstr>\n");
		exit (0);
	}

	last = (float**)malloc(maxcells * sizeof(float*));
	minvarsum = (float**)malloc(maxcells * sizeof(float*));
	minvaravg = (float**)malloc(maxcells * sizeof(float*));

	for(i=0;i<maxcells;i++){
		last[i] = (float*)malloc(maxyrs * sizeof(float));
		minvarsum[i] = (float*)malloc(maxyrs * sizeof(float));
		minvaravg[i] = (float*)malloc(maxyrs * sizeof(float));
	}

	wydminvar = (int**)malloc(maxcells * sizeof(int*));
	wydminmnth = (int**)malloc(maxcells * sizeof(int*));
	wydminday = (int**)malloc(maxcells * sizeof(int*));
	m12check = (int**)malloc(maxcells * sizeof(int*));

	for(i=0;i<maxcells;i++){
		wydminvar[i] = (int*)malloc(maxyrs * sizeof(int));
		wydminmnth[i] = (int*)malloc(maxyrs * sizeof(int));
		wydminday[i] = (int*)malloc(maxyrs * sizeof(int));
		m12check[i] = (int*)malloc(maxyrs * sizeof(int));
	}
	icell=0;

	/*read argument strings to integer values*/
	sscanf(argv[1],"%s", name[icell]);
	sscanf(argv[2],"%s", inpathstr);
	printf("inpathstr: %s\n", inpathstr);
	sscanf(argv[3],"%s", outpathstr);
	sscanf(argv[4],"%d", &begdatayear);
	sscanf(argv[5],"%d", &startyear);
	sscanf(argv[6],"%d", &endyear);
	sscanf(argv[8],"%d", &wymonth);

	/*open input file list*/

//	strcpy(temp,argv[1]);
//	filelist=fopen(temp, "r");
//	if(filelist==NULL) printf("error:  cannot open %s\n", temp);

	/*open output file*/
	strcpy(temp,outpathstr);
	strcat(temp,argv[7]);
	strcat(temp,"_strflw_7q10_stats");
	printf("outfile path is %s\n", temp);


	outputfile[0]=fopen(temp, "w");
	if(outputfile[0]==NULL) printf("error1:  cannot open %s\n", temp);

	/*loop over all input files in filelist, open file and extract peak flow in each water year*/

	// while(fscanf(filelist,"%s%f%f", name[icell], &lat[icell], &lon[icell]) != EOF){
	// while(fscanf(filelist,"%s%f%f", name[icell], &lat[icell], &lon[icell]) != EOF){

//	strcpy(temp,inpathstr);
	strcpy(temp,argv[2]);
	strcat(temp,name[icell]);
	// strcat(temp,".day");
	inputfile=fopen(temp, "r");
//	printf("outpathstr: %s\n", outpathstr);
//	printf("inpathstr: %s\n", inpathstr);
//	printf("argv[2]: %s\n", argv[2]);
//	printf("argv[7]: %s\n", argv[7]);
	if(inputfile==NULL) printf("error2:  cannot open %s\n", temp);

	printf("processing file %s\n", temp);
//	printf("processing file %s\n", name[icell]);

	/*open two cell specific output files*/

	strcpy(temp,outpathstr);
	strcat(temp,name[icell]);
	strcat(temp,"_quantiles");
	printf("outfile path is %s\n", temp);

	outputfile[2]=fopen(temp, "w");
	if(outputfile[2]==NULL) printf("error:  cannot open %s\n", temp);

	strcpy(temp,outpathstr);
	strcat(temp,name[icell]);
	strcat(temp,"_7q10_flow_date");
	printf("outfile path is %s\n", temp);

	outputfile[3]=fopen(temp, "w");
	if(outputfile[3]==NULL) printf("error:  cannot open %s\n", temp);

	strcpy(temp,outpathstr);
	strcat(temp,name[icell]);
	strcat(temp,"_7q10_cal_date");
	printf("outfile path is %s\n", temp);

	outputfile[4]=fopen(temp, "w");
	if(outputfile[4]==NULL) printf("error:  cannot open %s\n", temp);

	/*initialize the summaxvar and maxvar arrays and year counter*/
	/*
	for(i=0;i<7000;i++) {
	minvarsum[i] = 9999999;
	*/
	for(j=0;j<200;j++){
		minvarsum[icell][j] = 9999999;
		m12check[icell][j] = 0;
	}

	iyear = 0;

	for(q = 0; q < 7; q++) {
		last[icell][q] = 0;
		// sum7day[icell] += last[icell][q];
		sum7day[icell] = 0;
	}

	/* read date stamp from file to determine startyear and month
	note assumes data starts on the first of some month */

	fscanf(inputfile, "%d %d %d %f ", &date[0], &date[1], &date[2], &strflw);
//	 begdatamnth=10;
	 while (skipOn==1){
		 if (date[0] < begdatayear){
			 fscanf(inputfile, "%d %d %d %f ", &date[0], &date[1], &date[2], &strflw);
		 }
		 else if (date[1]==wymonth && date[2]==1){
			 skipOn=0;
//			 begdatamnth = date[1]-1;
		 }
	 	 else{
	 		 // Skip months before start wymnth (11=Nov.).
			 fscanf(inputfile, "%d %d %d %f ", &date[0], &date[1], &date[2], &strflw);
			 /* Keep 7-day array active even while skipping */
//			printf("%d %d %d\n", date[0], date[1], date[2]);
			sum7day[icell] += strflw;
			sum7day[icell] -= last[icell][0];

			for(q=0; q<6; q++){
			last[icell][q]=last[icell][q+1];
			//			printf("%7.2f ", last[icell][q]);
			}
			//		printf("%7.2f ", last[icell][6]);
			last[icell][6]=strflw;
			//		printf("%7.2f\n",last[icell][6]);

	 	 }

	 }

	/* begin reading data*/
	for(year = begdatayear; year <= endyear; year++){

		if((year % 4 == 0) && (((year % 100 == 0) && (year % 400 != 0)) == 0)){
			dpm[1] = 29;
			for(i=0;i<12;i++) jdm[i]= jdm3[i];
		}

		else{
			dpm[1] = 28;
			for(i=0;i<12;i++) jdm[i]= jdm2[i];
		}

		if(year == endyear) endmnth = wymonth;
		else endmnth = 12;

		if(year == begdatayear) begmnth = (wymonth-1);
		else begmnth = 0;

		for(mnth = begmnth; mnth < endmnth; mnth++){

			if((year > begdatayear || (year == begdatayear && mnth >= (wymonth-1)))){
				cmnth[mnth]++;
			} //count number of months used
			m12check[icell][iyear]+=1;

			for(day=1;day<=dpm[mnth];day++){

				if(mnth == (wymonth-1) && day == 1) {
					// printf("%d %f nisperos salvajes\n", year, minvarsum[icell][iyear]);
//					printf("%f\n",minvarsum[icell][iyear]);
					// On new WY, print out calendar date, WY, and lowest WY flow.
					// Alternative to day-in-WY time keeping.
					if(iyear>0){
						fprintf(outputfile[4],"%d %d %d %d %d %7.6f\n", caldate[0], caldate[1], caldate[2], year, m12check[icell][iyear], (minvarsum[icell][iyear]/7));
					}

					iyear++;  //increment the year counter on Oct 1
					m12check[icell][iyear]=0;

				}
				if(year==begdatayear && mnth == (wymonth-1) && day == 1) {
					printf("Already read WY start day during skipOn\n");
				}
				else{
					if(fscanf(inputfile, "%d %d %d %f ", &date[0], &date[1], &date[2], &strflw) != 4){
						printf ("error reading input file. exiting. \n"); exit(0);
					}
				}
//				if(year==begdatayear && mnth == (wymonth-1) && day < 7) {
//					// QUICKFIX: just amplify first days rather
//					for(q=0; q<7; q++){
//						sum7day[icell]+=strflw;
//					}
//				}
//				if{
//				printf("%d %d %d %f %f %f\n", date[0], date[1], date[2],  strflw, sum7day[icell], last[icell][0]);
//				sum7day[icell] += strflw;
//				sum7day[icell] -= last[icell][0];
//				}
				sum7day[icell] += strflw;
				sum7day[icell] -= last[icell][0];
//				printf("%d %d %d %f %f %f\n", date[0], date[1], date[2],  strflw, sum7day[icell], last[icell][0]);

				if(sum7day[icell] < minvarsum[icell][iyear]){
					minvarsum[icell][iyear] = sum7day[icell];
					wydminvar[icell][iyear] = jdm[mnth] + day;
					wydminmnth[icell][iyear] = jdm[mnth];
					wydminday[icell][iyear] = day;

					caldate[0] = date[0];
					caldate[1] = date[1];
					caldate[2] = date[2];
				}

				//incrementing sum factors
				for(q=0; q<6; q++){
					last[icell][q]=last[icell][q+1];
//					printf("%7.2f ", last[icell][q]);
				}
//				printf("%7.2f ", last[icell][6]);
				last[icell][6]=strflw;
//				printf("%7.2f, %7.2f, %7.2f\n",last[icell][6],sum7day[icell],minvarsum[icell][iyear]);
			}
		}
		// printf("%d %f los salvajes\n", year, minvarsum[icell][iyear]);
	}
//	exit(0);

//	numyears = iyear + 1;
//	sampsize = iyear;
	numyears = iyear;
	sampsize = iyear - 1;


	for(i=1;i<numyears;i++){
		minvaravg[icell][i] =  ((minvarsum[icell][i])/7);
	}


	/*write out annual flood peak and date for this cell*/
//	for(i=1;i<numyears;i++) fprintf(outputfile[3],"%d %7.1f %d %d %d\n",i, minvaravg[icell][i], wydminvar[icell][i], wydminmnth[icell][i], wydminday[icell][i]);
	for(i=1;i<numyears;i++){
		if(m12check[icell][i]==12)
			fprintf(outputfile[3],"%d %7.6f %d %d %d %d\n",i, minvaravg[icell][i], wydminvar[icell][i], wydminmnth[icell][i], wydminday[icell][i], m12check[icell][i]);
	}

	fclose(outputfile[3]);
	fclose(outputfile[4]);
	/* close input file and increment cell counter*/
	fclose(inputfile);

	/*make duplicate array for sorting*/

	for(i=1;i<numyears;i++){
		tempsort[i] = minvaravg[icell][i];
	}

	/*sort the maxvar array and load to processing array*/

	shellsort(sampsize, tempsort);

	for(i=1;i<numyears;i++){

		sort[i][0] = numyears - i;  //rank
		sort[i][1] = tempsort[i];   //ranked peak flow data
		sort[i][2] = (sort[i][0]-0.4) / (sampsize + 0.2); //exceedence probability based on Cunnane estimator

		fprintf(outputfile[2],"%4.0f %7.6f %4.5f\n", sort[i][0], sort[i][1],sort[i][2]);
		//printf("%4.0f %7.1f %4.5f\n", sort[i][0], sort[i][1],sort[i][2]);

	}

	fclose(outputfile[2]);

	/* calculate biased and unbiased prob weighted moments*/

	/*initialize variables*/
	for(i=0;i<15;i++){ B[i]=0; UB[i]=0; sum[i]=0;}
	for(i=0;i<2;i++){LN[i]=0; lnsum[i]=0;}

	for(i=1;i<numyears;i++){
		t1 = (1 - (sort[i][0]-0.35)/sampsize);
		B[0] += (double)sort[i][1]/sampsize;
		B[1] += (double)(sort[i][1]*t1)/sampsize;
		B[2] += (double)(sort[i][1]*t1*t1)/sampsize;
		B[3] += (double)(sort[i][1]*t1*t1*t1)/sampsize;
		B[4] += (double)(sort[i][1]*t1*t1*t1*t1)/sampsize;
		B[5] += (double)(sort[i][1]*t1*t1*t1*t1*t1)/sampsize;
		B[6] += (double)(sort[i][1]*t1*t1*t1*t1*t1*t1)/sampsize;
		B[7] += (double)(sort[i][1]*t1*t1*t1*t1*t1*t1*t1)/sampsize;
		B[8] += (double)(sort[i][1]*t1*t1*t1*t1*t1*t1*t1*t1)/sampsize;
		B[9] += (double)(sort[i][1]*t1*t1*t1*t1*t1*t1*t1*t1*t1)/sampsize;
		B[10] += (double)(sort[i][1]*t1*t1*t1*t1*t1*t1*t1*t1*t1*t1)/sampsize;

		// unbiased PWM estimators--note reversed rank order

		UB[0] += (double)sort[i][1]/sampsize;

		if(i >= 2) UB[1] += (double)((sampsize-sort[i][0])*sort[i][1]/(sampsize)/(sampsize -1));
		if(i >= 3) UB[2] += (double)((sampsize-sort[i][0])*(sampsize-sort[i][0]-1)*sort[i][1]/(sampsize)/(sampsize -1)/(sampsize -2));
		if(i >= 4) UB[3] += (double)((sampsize-sort[i][0])*(sampsize-sort[i][0]-1)*(sampsize-sort[i][0]-2)*sort[i][1]/(sampsize)/(sampsize -1)/(sampsize -2)/(sampsize -3));

		// log mean and standard deviation

		LN[0] += log(sort[i][1])/sampsize;
		lnsum[0] += log(sort[i][1]);
		lnsum[1] += log(sort[i][1])*log(sort[i][1]);
	}  //end of for loop


	LN[1] = sqrt((lnsum[1] - (lnsum[0]*lnsum[0]/sampsize))/(sampsize-1));

	for(i=0;i<2;i++) printf("LN %d = %f\n", i, LN[i]);
	for(i=0;i<4;i++)   printf("UB%d  = %f\n",i, UB[i]);
	printf("\n");

	/*calculate normalized PWM's for use in calculating LH moments*/

	for(i=0;i<11;i++){
		printf("B %d = %f\n", i, B[i]);
	}

	for(i=0;i<11;i++){
		NB[i] = (i+1)*B[i];
		printf("NB %d = %f\n", i, NB[i]);
	}

	/* calculate L moments */

	calc_lmoments = 1 ;

	// use biased estimators

	if(calc_lmoments == 0) {
		L[0] = B[0];
		L[1] = 2*B[1] - B[0];
		L[2] = 6*B[2] - 6*B[1] + B[0];
		L[3] = 20*B[3] -30*B[2] + 12*B[1] - B[0];

		for(i=0;i<4;i++)  printf("L %d = %f\n",i+1, L[i]);
	}

	/*use unbiased estimators*/

	if(calc_lmoments == 1) {
		L[0] = UB[0];
		L[1] = 2*UB[1] - UB[0];
		L[2] = 6*UB[2] - 6*UB[1] + UB[0];
		L[3] = 20*UB[3] -30*UB[2] + 12*UB[1] - UB[0];

		for(i=0;i<4;i++)  printf("L %d = %f\n",i+1, L[i]);
	}

	/*calculate LH2 moments (Wang 1997)*/

	LH2[0] = NB[2];
	LH2[1] = (double)2.0*(NB[3]- NB[2]);
	LH2[2] = (double)5.0/6.0 *(6.0 * NB[4] - 10.0 * NB[3] + 4.0 * NB[2]);
	LH2[3] = (double)0.25 * ( 56.0 * NB[5] - 126.0 * NB[4] + 90.0 * NB[3] - 20.0 * NB[2]);

	tau23 = LH2[2]/LH2[1];
	tau24 = LH2[3]/LH2[2];

	for(i=0;i<4;i++) printf("LH2 %d = %lf\n",i, LH2[i]);
	printf("tau23 =%lf tau24=%lf\n", tau23, tau24);

	/*calculate LH4 moments (Wang 1997)*/

	LH4[0] = NB[4];
	LH4[1] = (double)6.0/2.0*(NB[5]- NB[4]);
	LH4[2] = (double)7.0/6.0 *(8.0 * NB[6] - 14.0 * NB[5] + 6.0 * NB[4]);
	LH4[3] = (double)8.0/24.0 * ( 90.0 * NB[7] - 216.0* NB[6] + 168.0 * NB[5] - 42.0 * NB[4]);

	tau43 = LH4[2]/LH4[1];
	tau44 = LH4[3]/LH4[2];

	for(i=0;i<4;i++) printf("LH4 %d = %lf\n",i, LH4[i]);
	printf("tau43 =%lf tau44=%lf\n", tau43, tau44);

	/*fit GEV distribution using L moments*/
	//parameters for gamma function estimator see Handbook of hydrology pp 18.18

	gammafunc = 0;
	c = 2*L[1]/(L[2]+3*L[1]) - 0.630930;
	kappa[0] = 7.8590*c + 2.9554*c*c;
	gammafunc = gammafn2(1.0 + kappa[0]);
	alpha[0] = kappa[0]*L[1]/gammafunc/(1.0 - exp(-1*kappa[0]*log(2)));
	psi[0] = L[0] + alpha[0]/kappa[0] *(gammafunc -1);

	printf("L moments GEV:  gamma = %f kappa = %f alpha = %f psi = %f\n", gammafunc, kappa[0], alpha[0], psi[0]);

	/* calculate GEV parameters based on LH2 moments (Wang 1997)*/

	gammafunc = 0;
	a2[0] = 0.5914;
	a2[1] = -2.3351;
	a2[2] = 0.6442;
	a2[3] = -0.1616;
	kappa[1] = a2[0] + a2[1]*tau23 + a2[2]*tau23*tau23 + a2[3]*tau23*tau23*tau23;
	gammafunc = gammafn2(1.0 + kappa[1]);
	alpha[1] = LH2[1]/(2*gammafunc/kappa[1]*(exp(-1*kappa[1]*log(3.0)) - exp(-1*kappa[1]*log(4.0))));
	psi[1] = LH2[0]- alpha[1]/kappa[1]* (1.0 - gammafunc*exp(-1.0*kappa[1]*log(3.0)));
	printf("LH2 moments GEV: gamma = %f kappa = %f alpha = %f psi = %f\n", gammafunc, kappa[1], alpha[1], psi[1]);

	/* calculate GEV parameters based on LH4 moments (Wang 1997)*/

	gammafunc = 0;
	a4[0] = 0.7113;
	a4[1] = -2.5383;
	a4[2] = 0.5142;
	a4[3] = -0.1027;
	kappa[2] = a4[0] + a4[1]*tau43 + a4[2]*tau43*tau43 + a4[3]*tau43*tau43*tau43;
	gammafunc = gammafn2(1.0 + kappa[2]);
	alpha[2] = LH4[1]*2*kappa[2]/6.0/gammafunc/(exp(-1*kappa[2]*log(5.0)) - exp(-1*kappa[2]*log(6.0)));
	psi[2] = LH4[0]- alpha[2]/kappa[2]* (1.0 - gammafunc*exp(-1.0*kappa[2]*log(5.0)));
	printf("LH4 moments GEV: gamma = %f kappa = %f alpha = %f psi = %f\n", gammafunc, kappa[2], alpha[2], psi[2]);

	/*calculate EV1 parameters based on L moments*/
	alpha[3] = 1.443* L[1];
	psi[3] = L[0] - 0.5772*alpha[3];
	printf("L moments  EV1: alpha = %f psi = %f\n", alpha[3], psi[3]);

	/*calculate flood quantiles for all distributions and load to output arrays*/

	p[0] = 0.002; // 5000 year
	p[1] = 0.005; // 200 year
	p[2] = 0.010; // 100 year
	p[3] = 0.020; // 50 year
	p[4] = 0.050; // 20 year
	p[5] = 0.100; // 10 year
	p[6] = 0.500; // 2 year

	for(i=0;i<7;i++){
		zp = (exp(0.135*log(p[i])) - exp(0.135*log(1.0 - p[i])))/0.1975;
		// GEV with L, L2, L4 - moments
		for(j=0;j<3;j++){
			output[icell][j][i] = psi[j] + alpha[j]/kappa[j] * (1 - exp(kappa[j]*log(-1.0*log(p[i]))));
		}
		// L moments EV1
		output[icell][3][i] = psi[3] - alpha[3]*log(-1.0*log(p[i]));
		// LN3???
		output[icell][4][i] = exp( LN[0] + zp*LN[1]);
	}

	/*diagnostic printout*/

	for(i=0;i<7;i++){
		for(j=0;j<5;j++){
		//printf(" P = %f dist = %d xp = %f\n", p[i], j, output[icell][j][i]);
			continue;
		}
	}

	icell++;

	//} //end while loop

	numcells = icell;

	// printf("%d\n", numcells);


	/*write flood stats to the output files*/

	for(i=0;i<numcells;i++){
		for(j=0;j<5;j++){
			fprintf(outputfile[0],"%s dist %d ", name[i], j);
			for(k=0;k<7;k++) fprintf(outputfile[0],"%7.6f ", output[i][j][k]);
			fprintf(outputfile[0],"\n");
		}
	}

	//fclose(filelist);
	fclose(outputfile[0]);

//	exit(0);
//	puts("here");
	return (0);
} //end main

/* sorting routine from Numerical Receipes pg 332 */

void shellsort (int n, float a[]) {

	int i,j, inc;
	float v;

	inc = 1;

	do{
		inc *= 3;
		inc++;
	} while(inc <= n);

	do{
		inc /= 3;
		for(i=inc+1;i<=n;i++) {
			v=a[i];
			j=i;
			while(a[j-inc] > v) {
				a[j]=a[j-inc];
				j -= inc;
				if (j <= inc) break;
			}
			a[j] = v;
		}
	} while(inc >1);
} //end shellsort


double gammafn2(float xx) {  

	/* This function calculates the ln of the gamma function using the tgamma() or lgamma function in the C library and returns exp(lgamma(x)) Note positive or negative arguments permitted but accuracy for negative arguments somewhat diminished*/

	double y, gammaln;
	y = (double)xx;
	if( y > 0) return tgamma(y);
	else {
		gammaln = lgamma(y);
		return signgam*exp(gammaln);
	}
} //end gammafn2  
