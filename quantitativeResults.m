r = cell(4);
r{1} = imread('Images/r1RGB.png');
r{2} = imread('Images/r2RGB.png');
r{3} = imread('Images/r3RGB.png');
r{4} = imread('Images/r4RGB.png');

mak = cell(4);
mak{1} = imread('Images/r1 Masato Akai''s Method.tiff');
mak{2} = imread('Images/r2 Masato Akai''s Method.tiff');
mak{3} = imread('Images/r3 Masato Akai''s Method.tiff');
mak{4} = imread('Images/r4 Masato Akai''s Method.tiff');

% r1_mak_sharp = cell(1);
% r1_mak_sharp{1} = imread('Images/r1 mAk + PCGF_Sharp(a=1)+Fusion.png');
% r1_mak_sharp{2} = imread('Images/mAk_vs_mAk+CLAHE(c=2)+Fusion.png');
% r1_mak_sharp{3} = imread('Images/mAk_vs_mAk+CLAHE(c=2).png');
% r1_mak_sharp{4} = imread('Images/mAk_vs_mAk+CLAHE(c=6).png');

clahe = cell(4);
clahe{1} = imread('Images/r1 mAk + CLAHE(c=2).png');
clahe{2} = imread('Images/r2 MAk(y=2) + CLAHE(c=2).tiff');
clahe{3} = imread('Images/r3 MAk(y=2) + CLAHE(c=2).tiff');
clahe{4} = imread('Images/r4 MAk(y=2) + CLAHE(c=2).tiff');

claheF = cell(4);
claheF{1} = imread('Images/r1 MAk(y=2) + CLAHE(c=2) + Fusion.tiff');
claheF{2} = imread('Images/r2 MAk(y=2) + CLAHE(c=2) + Fusion.tiff');
claheF{3} = imread('Images/r3 MAk(y=2) + CLAHE(c=2) + Fusion.tiff');
claheF{4} = imread('Images/r4 MAk(y=2) + CLAHE(c=2) + Fusion.tiff');

claheFy26 = cell(4);
claheFy26{1} = imread('Images/r1 MAk(y=2.6) + CLAHE(c=2) + Fusion.tiff');
claheFy26{2} = imread('Images/r2 MAk(y=2.6) + CLAHE(c=2) + Fusion.tiff');
claheFy26{3} = imread('Images/r3 MAk(y=2.6) + CLAHE(c=2) + Fusion.tiff');
claheFy26{4} = imread('Images/r4 MAk(y=2.6) + CLAHE(c=2) + Fusion.tiff');

claheFy16 = cell(4);
claheFy16{1} = imread('Images/r1 MAk(y=1.66) + CLAHE(c=2) + Fusion.tiff');
claheFy16{2} = imread('Images/r2 MAk(y=1.16) + CLAHE(c=2) + Fusion.tiff');
claheFy16{3} = imread('Images/r3 MAk(y=1.22) + CLAHE(c=2) + Fusion.tiff');
claheFy16{4} = imread('Images/r4 MAk(y=1.24) + CLAHE(c=2) + Fusion.tiff');

claheF3 = cell(4);
claheF3{1} = imread('Images/r1 MAk(y=2) + CLAHE(c=2) + Fusion3.tiff');
claheF3{2} = imread('Images/r2 MAk(y=2) + CLAHE(c=2) + Fusion3.tiff');
claheF3{3} = imread('Images/r3 MAk(y=2) + CLAHE(c=2) + Fusion3.tiff');
claheF3{4} = imread('Images/r4 MAk(y=2) + CLAHE(c=2) + Fusion3.tiff');

clahey16 = cell(4);
clahey16{1} = imread('Images/r1 MAk(y=1.66) + CLAHE(c=2).tiff');
clahey16{2} = imread('Images/r2 MAk(y=1.16) + CLAHE(c=2).tiff');
clahey16{3} = imread('Images/r3 MAk(y=1.22) + CLAHE(c=2).tiff');
clahey16{4} = imread('Images/r4 MAk(y=1.24) + CLAHE(c=2).tiff');

rNIQE = [1:4];
makNIQE = [1:4];
res = [1:4];
claheNIQE = [1:4];
claheFNIQE = [1:4];
claheFy26NIQE = [1:4];
claheFy16NIQE = [1:4];
clahey16NIQE = [1:4];
claheF3NIQE = [1:4];

for i = 1:4
    rNIQE(i) = niqe(r{i});
    makNIQE(i) = niqe(mak{i});
%     res(i) = niqe(r1_mak_sharp{i});
    claheNIQE(i) = niqe(clahe{i});
    claheFNIQE(i) = niqe(claheF{i});
    claheFy26NIQE(i) = niqe(claheFy26{i});
    claheFy16NIQE(i) = niqe(claheFy16{i});
    clahey16NIQE(i) = niqe(clahey16{i});
    claheF3NIQE(i) = niqe(claheF3{i});
end

disp("Our results:")
disp("Displaying NIQE results:")
Image = [1;2;3;4];
T = table(Image, rNIQE', makNIQE', claheNIQE', claheFy26NIQE', claheF3NIQE');
T.Properties.VariableNames = {'Image' 'Original' 'Masato Akai' 'CLAHE' 'CLAHE+Fusion+y=2.6' 'CLAHE+Fusion3'};
T

for i = 1:4
    rNIQE(i) = piqe(r{i});
    makNIQE(i) = piqe(mak{i});
%     res(i) = piqe(r1_mak_sharp{i});
    claheNIQE(i) = piqe(clahe{i});
    claheFNIQE(i) = piqe(claheF{i});
    claheFy26NIQE(i) = piqe(claheFy26{i});
    claheFy16NIQE(i) = piqe(claheFy16{i});
    clahey16NIQE(i) = piqe(clahey16{i});
    claheF3NIQE(i) = piqe(claheF3{i});
end

disp("Displaying PIQE results:")
T = table(Image, rNIQE', makNIQE', claheNIQE', claheFy26NIQE', claheF3NIQE');
T.Properties.VariableNames = {'Image' 'Original' 'Masato Akai' 'CLAHE' 'CLAHE+Fusion+y=2.6' 'CLAHE+Fusion3'};
T

mak = cell(4);
mak{1} = imread('YourResults/r1 Masato Akai''s Method.png');
mak{2} = imread('YourResults/r2 Masato Akai''s Method.png');
mak{3} = imread('YourResults/r3 Masato Akai''s Method.png');
mak{4} = imread('YourResults/r4 Masato Akai''s Method.png');

clahe = cell(4);
clahe{1} = imread('YourResults/r1 MAk + CLAHE.png');
clahe{2} = imread('YourResults/r2 MAk + CLAHE.png');
clahe{3} = imread('YourResults/r3 MAk + CLAHE.png');
clahe{4} = imread('YourResults/r4 MAk + CLAHE.png');

claheF = cell(4);
claheF{1} = imread('YourResults/r1 MAk + CLAHE + Fusion.png');
claheF{2} = imread('YourResults/r2 MAk + CLAHE + Fusion.png');
claheF{3} = imread('YourResults/r3 MAk + CLAHE + Fusion.png');
claheF{4} = imread('YourResults/r4 MAk + CLAHE + Fusion.png');

claheF3 = cell(4);
claheF3{1} = imread('YourResults/r1 MAk + CLAHE + Fusion3.png');
claheF3{2} = imread('YourResults/r2 MAk + CLAHE + Fusion3.png');
claheF3{3} = imread('YourResults/r3 MAk + CLAHE + Fusion3.png');
claheF3{4} = imread('YourResults/r4 MAk + CLAHE + Fusion3.png');

rNIQE = [1:4];
makNIQE = [1:4];
claheNIQE = [1:4];
claheFNIQE = [1:4];
claheF3NIQE = [1:4];

for i = 1:4
    rNIQE(i) = niqe(r{i});
    makNIQE(i) = niqe(mak{i});
    claheNIQE(i) = niqe(clahe{i});
    claheFNIQE(i) = niqe(claheF{i});
    claheF3NIQE(i) = niqe(claheF3{i});
end

disp("");disp("");disp("");
disp("Displaying Your results:")
disp("Displaying NIQE results:")
Image = [1;2;3;4];
T = table(Image, rNIQE', makNIQE', claheNIQE', claheF3NIQE');
T.Properties.VariableNames = {'Image' 'Original' 'Masato Akai' 'CLAHE' 'CLAHE+Fusion3'};
T

for i = 1:4
    rNIQE(i) = piqe(r{i});
    makNIQE(i) = piqe(mak{i});
%     res(i) = piqe(r1_mak_sharp{i});
    claheNIQE(i) = piqe(clahe{i});
    claheFNIQE(i) = piqe(claheF{i});
    claheFy26NIQE(i) = piqe(claheFy26{i});
    claheFy16NIQE(i) = piqe(claheFy16{i});
    clahey16NIQE(i) = piqe(clahey16{i});
    claheF3NIQE(i) = piqe(claheF3{i});
end

disp("Displaying PIQE results:")
T = table(Image, rNIQE', makNIQE', claheNIQE', claheF3NIQE');
T.Properties.VariableNames = {'Image' 'Original' 'Masato Akai' 'CLAHE' 'CLAHE+Fusion3'};
T
