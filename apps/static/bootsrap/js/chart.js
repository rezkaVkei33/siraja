document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/chart-data/')
        .then(response => response.json())
        .then(data => {
            // Pastikan elemen 'angkutanChart' ada
            const ctxAngkutanElement = document.getElementById('angkutanChart');
            if (ctxAngkutanElement) {
                const ctxAngkutan = ctxAngkutanElement.getContext('2d');
                const jenisAngkutan = data.jenis_angkutan || [];
                const angkutanCounts = data.angkutan_counts || [];

                const angkutanChart = new Chart(ctxAngkutan, {
                    type: 'bar',
                    data: {
                        labels: jenisAngkutan,
                        datasets: [{
                            label: 'Jumlah Angkutan',
                            backgroundColor: '#4e73df',
                            data: angkutanCounts,
                        }],
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            } else {
                console.error("Element 'angkutanChart' tidak ditemukan di halaman.");
            }

            // Pastikan elemen 'penumpangChart' ada
            const ctxPenumpangElement = document.getElementById('penumpangChart');
            if (ctxPenumpangElement) {
                const ctxPenumpang = ctxPenumpangElement.getContext('2d');
                const namaSopir = data.nama_sopir || [];
                const penumpangNaik = data.penumpang_naik || [];
                const penumpangTurun = data.penumpang_turun || [];

                const penumpangChart = new Chart(ctxPenumpang, {
                    type: 'bar',
                    data: {
                        labels: namaSopir,
                        datasets: [
                            {
                                label: 'Jumlah Naik',
                                backgroundColor: '#1cc88a',
                                data: penumpangNaik,
                            },
                            {
                                label: 'Jumlah Turun',
                                backgroundColor: '#e74a3b',
                                data: penumpangTurun,
                            }
                        ],
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            } else {
                console.error("Element 'penumpangChart' tidak ditemukan di halaman.");
            }
        })
        .catch(error => {
            console.error("Error fetching chart data:", error);
        });
});
