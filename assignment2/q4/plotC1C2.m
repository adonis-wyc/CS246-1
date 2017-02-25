c1_eud = importdata('c1_eud.txt');
c2_eud = importdata('c2_eud.txt');
c1_man = importdata('c1_man.txt');
c2_man = importdata('c2_man.txt');

close all;

x = 1 : 1 : 20;
figure;clf;
plot(x, c1_eud, '-o');
hold all;
plot(x, c2_eud, '->');
grid on;
xlabel('Iterations','fontsize', 15);
ylabel('\Phi','fontsize', 15)
legend('c1', 'c2');
title('\Phi vs Iter','fontsize', 15)
set(gca,'FontSize',20);

figure;clf;
plot(x, c1_man, '-s');
hold all;
plot(x, c2_man, '-<');
grid on;
xlabel('Iterations', 'fontsize',15);
ylabel('\Psi', 'fontsize', 15);
legend('c1', 'c2');
title('\Psi vs Iter', 'fontsize', 15);
set(gca,'FontSize',15);

