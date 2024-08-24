document.addEventListener("DOMContentLoaded", function () {
    fetch('/api/penumpang-pertahun/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Pastikan data tidak null atau undefined
            const tahunLabels = data.tahun_labels || [];
            const jumlahNaik = data.jumlah_naik || [];
            const jumlahTurun = data.jumlah_turun || [];

            // Pastikan elemen 'penumpangPerTahunChart' ada di halaman
            const ctxElement = document.getElementById('penumpangPerTahunChart');
            if (ctxElement) {
                const ctx = ctxElement.getContext('2d');

                const penumpangPerTahunChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: tahunLabels,
                        datasets: [
                            {
                                label: 'Jumlah Naik',
                                backgroundColor: '#1c8cc8',
                                data: jumlahNaik,
                            },
                            {
                                label: 'Jumlah Turun',
                                backgroundColor: '#4ac81c',
                                data: jumlahTurun,
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
                console.error("Element 'penumpangPerTahunChart' tidak ditemukan di halaman.");
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
});
